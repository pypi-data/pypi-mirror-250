import json
import threading
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, List

from async_schedule.op import TaskOperator

T = TypeVar('T')


class AbstractWorker(ABC, Generic[T]):

    def __init__(self, max_running_task_num=5):
        self.max_running_task_num = max_running_task_num
        self.cur_running_task_num = 0
        self.lock = threading.Lock()

    def get_max_running_task_num(self):
        return self.max_running_task_num

    def increase_running_task_num(self):
        with self.lock:
            if self.cur_running_task_num < self.max_running_task_num:
                self.cur_running_task_num += 1

    def decrease_running_task_num(self):
        with self.lock:
            if self.cur_running_task_num > 0:
                self.cur_running_task_num -= 1

    def enable_pull_new_task(self):
        with self.lock:
            if self.cur_running_task_num < self.max_running_task_num:
                return True
            else:
                return False

    @abstractmethod
    def work(self, op: TaskOperator, task_context: T):
        pass

    @abstractmethod
    def get_task_context_type(self) -> Type[T]:
        pass

    @staticmethod
    def retryable(exception_instance):
        return True  # 默认均可以重试

    @staticmethod
    def marshal(task_context: T) -> str:
        return json.dumps(task_context.__dict__)

    @staticmethod
    def unmarshal(task_context_str: str, cls: Type[T]) -> T:
        data = json.loads(task_context_str)
        return cls(**data)
