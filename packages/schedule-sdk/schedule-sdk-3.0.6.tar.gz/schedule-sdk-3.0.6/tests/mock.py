from abc import ABC
from typing import Type

from async_schedule.client import TaskRpcInterface
from async_schedule.domain import Task
from async_schedule.op import TaskOperator
from async_schedule.worker import AbstractWorker


class MockTaskRpcClient(TaskRpcInterface):
    def submit_task(self, task):
        # Mock实现，可以根据需要进行具体实现
        print(f"Mock: Submitting task {task.__dict__}")

    def hold_task(self, task_id) -> Task:
        # Mock实现，可以根据需要进行具体实现
        print(f"Mock: Getting task {task_id}")
        return Task(task_type=mock_task_type, context=mock_nums_str)

    def update_task(self, task_id, req):
        # Mock实现，可以根据需要进行具体实现
        print(f"Mock: Updating task:{task_id},  {req.__dict__}")


class MockWorkContext:
    def __init__(self, nums: []):
        self.nums = nums


class MockWorker(AbstractWorker[MockWorkContext], ABC):
    def get_task_context_type(self) -> Type[MockWorkContext]:
        return MockWorkContext

    def work(self, op: TaskOperator, task_context: MockWorkContext):
        print(sum(task_context.nums))

    @staticmethod
    def retryable(exception_instance):
        return IOError


mock_task_type = "mock"
mock_worker = MockWorker()

mock_nums = [1, 2, 3]
mock_nums_str = '{"nums": [1, 2, 3]}'
mock_task_ctx = MockWorkContext(mock_nums)

mock_task = Task(mock_task_type, mock_nums_str)
mock_task_client = MockTaskRpcClient()
