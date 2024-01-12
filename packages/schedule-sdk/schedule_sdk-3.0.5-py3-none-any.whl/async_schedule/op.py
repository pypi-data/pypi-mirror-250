import json
import time

from async_schedule.client import TaskRpcInterface, UpdateTaskReq
from async_schedule.domain import Task, TaskStatus, stage_progress_update_fields


class TaskOperator:
    """
    暴露给业务逻辑中对task的操作接口
    """

    def __init__(self, task: Task,
                 task_client: TaskRpcInterface,
                 context_serializer):
        self.task = task
        self.task_client = task_client
        self.context_serializer = context_serializer

    # ======== 阶段 ========
    def get_stage(self) -> str:
        return self.task.stage

    def set_stage(self, stage: str):
        self.task.stage = stage
        self.task_client.update_task(self.task.task_id, UpdateTaskReq(["Stage"], self.task))

    def wait_next_stage(self, ctx, next_stage: str, next_stage_progress: float = 0):
        """
        当前阶段结束，手动指定下一执行的阶段
        调用该方法后，需要在业务代码中return

        :param ctx: 任务指定上下文
        :param next_stage: 下一阶段
        :param next_stage_progress: 下一阶段的进度
        """
        if next_stage_progress <= 0 or next_stage_progress >= 1:
            raise ValueError("下一阶段进度必须在(0,1)之间")

        self.task.stage = next_stage
        self.task.stage_progress = next_stage_progress  # 阶段的进度默认为0

        self.task.retry_index = 0  # 该阶段成功，将重试次数置为0
        self.task.context = self.context_serializer(ctx)
        self.task.status = TaskStatus.WAIT_FOR_NEXT_STAGE
        self.task.on_update()

        # self.task_client.update_task(self.task.task_id, UpdateTaskReq(stage_change_fields, self.task))

    # ======== 保存当前阶段进度 ========
    def remote_save_stage_progress(self, ctx, cur_stage_progress: float):
        """
        :param ctx: 任务指定上下文
        :param cur_stage_progress: 当前阶段的进度
        """
        if cur_stage_progress <= 0 or cur_stage_progress >= 1:
            raise ValueError("当前阶段进度必须在(0,1)之间")

        self.task.stage_progress = cur_stage_progress
        self.task.context = self.context_serializer(ctx)

        self.task_client.update_task(self.task.task_id, UpdateTaskReq(stage_progress_update_fields, self.task))

    # ======== 日志 ========
    MAX_LOG_ENTRIES = 50  # 限制日志条目数量

    def log_info(self, message):
        self._log("info", message)

    def log_error(self, message):
        self._log("error", message)

    def log_warn(self, message):
        self._log("warn", message)

    def _log(self, level, message):
        """
        Internal method for logging a message at a specified level.
        """
        log_entry = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "level": level,
                     "message": message}
        log_str = json.dumps(log_entry)
        self.task.log.append(log_str)

        # 限制日志条目数量
        if len(self.task.log) > self.MAX_LOG_ENTRIES:
            self.task.log = self.task.log[-self.MAX_LOG_ENTRIES:]
