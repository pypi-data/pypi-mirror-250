import time
import uuid
from dataclasses import dataclass
from enum import IntEnum


class TaskStatus(IntEnum):
    CREATED = 1
    WAIT_FOR_RETRY = 2
    WAIT_FOR_NEXT_STAGE = 3
    SCHEDULED = 8
    RUNNING = 9
    FINAL = 10
    FAILED = 11
    SUCCESS = 12


stage_progress_update_fields = ["StageProgress", "Context"]
status_update_fields = ["Log", "Status", "RetryIndex", "Context", "ModifyTime", "OrderTime"]
stage_change_fields = status_update_fields[:] + ["Stage", "StageProgress"]


@dataclass
class Task:
    def __init__(self, task_type: str, context: str,
                 user_id=None, task_id=None, version=None, max_retry_num=None,
                 retry_interval=None, max_running_num=None, priority=None,
                 stage_conf=None, stage=None, stage_progress=None, status=None,
                 retry_index=None, log=None, order_time=None, create_time=None,
                 modify_time=None):

        self.task_type = task_type
        self.context = context

        self.user_id = "default" if user_id is None else user_id
        self.task_id = str(uuid.uuid4()) if task_id is None else task_id
        self.version = 0 if version is None else version
        self.max_retry_num = 5 if max_retry_num is None else max_retry_num
        self.retry_interval = [100, 200, 300, 500, 1000] if retry_interval is None else retry_interval
        self.max_running_num = 10 if max_running_num is None else max_running_num
        self.priority = 0 if priority is None else priority
        self.stage_conf = "" if stage_conf is None else stage_conf
        self.stage = "" if stage is None else stage
        self.stage_progress = 0 if stage_progress is None else stage_progress
        self.status = TaskStatus.CREATED if status is None else status
        self.retry_index = 0 if retry_index is None else retry_index
        self.log = [] if log is None else log

        now = int(time.time())
        self.order_time = now if order_time is None else order_time
        self.create_time = now if create_time is None else create_time
        self.modify_time = now if modify_time is None else modify_time

    def on_update(self):
        self.modify_time = int(time.time())
        self.reset_order_time()

    def reset_order_time(self):
        if self.status == TaskStatus.CREATED:
            # Not yet scheduled
            self.order_time = self.create_time - self.priority
        elif self.status == TaskStatus.WAIT_FOR_NEXT_STAGE:
            self.order_time = self.modify_time - self.priority
        elif self.status == TaskStatus.WAIT_FOR_RETRY:
            self.order_time = self.modify_time + self.retry_interval[self.retry_index]
