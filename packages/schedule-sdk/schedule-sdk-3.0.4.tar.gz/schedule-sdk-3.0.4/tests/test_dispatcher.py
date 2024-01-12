import threading
import unittest

from async_schedule import dispatcher
from tests.mock import mock_task_client, mock_worker, mock_task_type


class TestTaskDispatcher(unittest.TestCase):
    def setUp(self):
        # 在每个测试方法之前建立redis连接
        self.dispatcher = dispatcher.TaskDispatcher(mock_task_client, redis_pass="123456", redis_host="127.0.0.1")
        self.dispatcher.redis_client.ping()

    def tearDown(self):
        # 在每个测试方法之后关闭连接
        self.dispatcher.redis_client.close()

    def test_register_task_worker(self):
        self.dispatcher.register_task_worker({mock_task_type: mock_worker})
        self.assertEqual(self.dispatcher.get_task_worker(mock_task_type), mock_worker)

    # def test_work(self):
    #     self.async_put_task()
    #     self.dispatcher.register_task_worker({mock_task_type: mock_worker})
    #     self.dispatcher.work()

    def async_put_task(self):
        def my_task():
            self.dispatcher.redis_client.lpush(mock_task_type, "123")

        # 创建一个 Thread 实例，并传入目标函数（即要在新线程中执行的任务）
        my_thread = threading.Thread(target=my_task)

        # 启动线程
        my_thread.start()
