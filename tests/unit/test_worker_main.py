"""
Worker main entry point tests module
"""
from unittest import TestCase
from unittest.mock import patch

from worker.main import main


class TestWorkerMain(TestCase):
    """
    Worker main entry point test cases implementation
    """
    TEST_PROFILE = 'test'

    @patch('worker.main.build_redis_url')
    @patch('worker.main.config')
    @patch('worker.main.register_exception_tracking')
    @patch('worker.main.register_instrumentation')
    @patch('worker.main.Client')
    @patch('worker.main.add_logstash_handler')
    @patch('worker.main.initialize_summary_service')
    @patch('worker.main.CELERY_APP')
    @patch('worker.main.PyLoader')
    @patch('worker.main.load_config')
    def test_main(self, load_config_mock, py_loader_mock, celery_app_mock, *_):
        """
        Test the main entry point runner calls the minimum required actors

        """
        main(self.TEST_PROFILE)

        load_config_mock.assert_called_with(self.TEST_PROFILE)
        py_loader_mock().load.assert_called_once()
        celery_app_mock.configure.assert_called_once()
        celery_app_mock.run.assert_called_once()
