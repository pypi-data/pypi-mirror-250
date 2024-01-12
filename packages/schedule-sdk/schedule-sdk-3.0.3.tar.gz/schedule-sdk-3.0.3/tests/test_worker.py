import unittest

from tests.mock import MockWorkContext, mock_nums, mock_worker, mock_nums_str


class TestAbstractWorker(unittest.TestCase):
    def test_marshal(self):
        ctx = MockWorkContext(mock_nums)
        ctx_str = mock_worker.marshal(ctx)

        self.assertEqual(ctx_str, mock_nums_str)

    def test_unmarshal(self):
        ctx = mock_worker.unmarshal(mock_nums_str, MockWorkContext)
        self.assertListEqual(ctx.nums, mock_nums)

    def test_work(self):
        ctx = mock_worker.unmarshal(mock_nums_str, MockWorkContext)
        mock_worker.work(None, ctx)

    def test_get_task_context_type(self):
        type_ = mock_worker.get_task_context_type()
        self.assertEqual(type_, MockWorkContext)


if __name__ == '__main__':
    unittest.main()
