import random
import time
from concurrent.futures.thread import ThreadPoolExecutor

import redis

from async_schedule.client import TaskRpcInterface, UpdateTaskReq
from async_schedule.domain import TaskStatus, stage_change_fields, status_update_fields
from async_schedule.op import TaskOperator
from async_schedule.worker import AbstractWorker


class TaskDispatcher:
    def __init__(self, task_client: TaskRpcInterface,
                 redis_host, redis_port=6379, db=0, redis_pass=""):
        self.max_worker_thread_num = 0
        self.executor = None

        self.redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=db,
            password=redis_pass
        )
        self.redis_client.ping()
        self.task_worker_map = {}
        self.task_client = task_client

    # ==================== worker注册 ====================

    # task_workers 为不定长参数
    # 传入参数为task_type对应的AbstractWorker
    def register_task_worker(self, *task_workers: {str: AbstractWorker}):

        for task_mapping in task_workers:
            for task_name, worker_instance in task_mapping.items():
                if not isinstance(worker_instance, AbstractWorker):
                    raise ValueError(
                        f"The value associated with task '{task_name}' must be an instance of AbstractWorker.")
                self.task_worker_map[task_name] = worker_instance
                self.max_worker_thread_num += worker_instance.get_max_running_task_num()

        self.executor = ThreadPoolExecutor(max_workers=min(self.max_worker_thread_num, 20))

    def get_task_worker(self, task_type: str) -> AbstractWorker:
        return self.task_worker_map.get(task_type)

    # ==================== 任务状态更新 ====================
    def _remote_process_error(self, op: TaskOperator):
        if op.task.retry_index >= op.task.max_retry_num:  # 达到最大重试次数
            self._remote_on_failed(op)
        else:
            # 未达到最大重试次数
            self._remote_on_retry(op)

    def _remote_on_retry(self, op: TaskOperator):
        op.task.status = TaskStatus.WAIT_FOR_RETRY
        op.task.retry_index += 1
        op.log_warn("任务执行失败，等待重试")
        op.task.on_update()
        self._remote_update_status(op)

    def _remote_on_failed(self, op: TaskOperator):
        op.task.status = TaskStatus.FAILED
        op.log_error("任务达到最大重试次数，执行失败")
        op.task.on_update()
        self._remote_update_status(op)

    def _remote_on_success(self, op: TaskOperator):
        op.task.status = TaskStatus.SUCCESS
        op.log_info("任务执行成功")
        op.task.on_update()
        self._remote_update_status(op)

    def _remote_update_status(self, op: TaskOperator):
        self.task_client.update_task(op.task.task_id,
                                     UpdateTaskReq(self._task_status_update_fields(), op.task))

    def _remote_update_stage(self, op: TaskOperator):
        self.task_client.update_task(op.task.task_id,
                                     UpdateTaskReq(stage_change_fields, op.task))

    @staticmethod
    def _task_status_update_fields():
        return status_update_fields

    # ==================== 分发执行 ====================
    def work(self):
        while True:
            free_queues = self._locked_listen_free_task_queues()
            if len(free_queues) == 0:  # 没有空闲的worker
                time.sleep(1)
                continue
            # 废弃
            # 使用blpop阻塞监听空闲任务队列，但阻塞一直占用长连接，不适合长时间阻塞
            # 从redis中获取一个空闲的任务类型
            # key, value = self.redis_client.blpop(free_queues, timeout=0)
            # key = key.decode('utf-8')

            # 打乱任务类型的顺序，避免某个任务类型的任务一直被优先执行
            random.shuffle(free_queues)
            key, value = None, None
            for task_type in free_queues:
                value = self.redis_client.lpop(task_type)
                if value is not None:
                    key = task_type
                    break
            if key is None:
                # 没有空闲的任务类型
                time.sleep(1)
                continue
            # 根据返回的键找到对应的 AbstractWorker 实例
            worker_instance = self.get_task_worker(key)

            if not worker_instance:
                continue

            task_id = value.decode('utf-8')
            print(
                f"[TaskDispatcher] [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] try hold task {task_id}, type: {key}")
            # 从task_server获取task domain对象
            try:
                task_data = self.task_client.hold_task(task_id)
                if not task_data:
                    print(
                        f"[TaskDispatcher] [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] task {task_id} not found")
                    continue
            except RuntimeError as e:
                print(
                    f"[TaskDispatcher] [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] hold task failed: {str(e)}"
                )
                continue

            op = TaskOperator(task_data, self.task_client, worker_instance.marshal)
            try:
                # 反序列化异步任务执行上下文
                task_context = worker_instance.unmarshal(task_data.context, worker_instance.get_task_context_type())
            except BaseException as e:
                op.log_error(f"unmarshal task_context: {task_data.context}, error: {str(e)}")
                self._remote_on_failed(op)
                continue

            self._locked_increase_running_task_num(key)

            print(
                f"[TaskDispatcher] [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] submitted task {task_id}")
            self.executor.submit(self._async_work, worker_instance, op, key, task_context)

    def _async_work(self, worker_instance: AbstractWorker, op: TaskOperator, task_type: str, task_context):
        try:
            print(
                f"[TaskDispatcher] [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] task {op.task.__dict__} work start")
            # 调用 worker 的 work 方法
            worker_instance.work(op, task_context)

            if op.task.status == TaskStatus.WAIT_FOR_NEXT_STAGE:
                # 没有发生异常，等待下一阶段调度
                self._remote_update_stage(op)
            else:
                # 没有发生异常，且不是等待下一阶段调度执行成功
                print(f"[Task-{op.task.task_id}] success")
                self._remote_on_success(op)
        except BaseException as e:
            print(f"[Task-{op.task.task_id}] failed: {str(e)}")
            op.log_error(f"task_context: {task_context}, error: {str(e)}")
            if not worker_instance.retryable(e):  # 发生不可重试的异常
                self._remote_on_failed(op)
                return
            self._remote_process_error(op)
        finally:
            self._locked_decrease_running_task_num(task_type)

    def _locked_listen_free_task_queues(self):
        free_types = [task_type for task_type, worker in self.task_worker_map.items()
                      if worker.enable_pull_new_task()]
        return free_types

    def _locked_increase_running_task_num(self, task_type):
        self.task_worker_map[task_type].increase_running_task_num()

    def _locked_decrease_running_task_num(self, task_type):
        self.task_worker_map[task_type].decrease_running_task_num()
