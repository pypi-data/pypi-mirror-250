import unittest

from async_schedule import op
from tests.mock import mock_task, mock_task_client, mock_worker, mock_task_ctx


class TestTaskOp(unittest.TestCase):
    def test_log_limit(self):
        self.mock_task_op = op.TaskOperator(mock_task, mock_task_client, mock_worker.marshal)
        for i in range(op.TaskOperator.MAX_LOG_ENTRIES):
            self.mock_task_op.log_error("test")
            self.assertEqual(i + 1, len(self.mock_task_op.task.log))

        for j in range(5):
            self.assertEqual(op.TaskOperator.MAX_LOG_ENTRIES, len(self.mock_task_op.task.log))

    def test_remote_save_stage_progress(self):
        self.mock_task_op = op.TaskOperator(mock_task, mock_task_client, mock_worker.marshal)

        mock_task_ctx.nums = [1, 2, 3, 4]

        self.mock_task_op.remote_save_stage_progress(mock_task_ctx, 0.5)
        self.assertEqual(self.mock_task_op.task.stage_progress, 0.5)
        self.assertEqual(self.mock_task_op.task.context, mock_worker.marshal(mock_task_ctx))

