import unittest
from unittest.mock import MagicMock, patch
from main import main

class TestMain(unittest.TestCase):
    @patch('main.parse_arguments')
    @patch('main.CSVManager')
    @patch('main.LockManager')
    @patch('main.Redis')
    @patch('main.time.sleep')
    def test_main_success(self, mock_sleep, mock_redis, mock_lock_manager, mock_csv_manager, mock_parse_arguments):
        # Mock the necessary objects and methods
        mock_args = MagicMock()
        mock_args.data = 'Test message'
        mock_args.sleep = 5
        mock_args.skip_release = False
        mock_parse_arguments.return_value = mock_args

        mock_redis_instance = MagicMock()
        mock_redis.from_url.return_value = mock_redis_instance

        mock_lock_manager_instance = MagicMock()
        mock_lock_manager.return_value = mock_lock_manager_instance
        mock_lock_manager_instance.acquire_lock.return_value = ('lock_key', 'lock_value')

        mock_csv_manager_instance = MagicMock()
        mock_csv_manager.return_value = mock_csv_manager_instance

        # Call the main function
        main()

        # Assert that the expected methods were called with the correct arguments
        mock_parse_arguments.assert_called_once()
        mock_redis.from_url.assert_called_once_with('REDIS_CONN_STR')
        mock_lock_manager.assert_called_once_with('REDIS_CONN_STR')
        mock_csv_manager.assert_called_once_with('REDIS_CSV_FILE_NAME', mock_redis_instance)
        mock_lock_manager_instance.acquire_lock.assert_called_once()
        mock_sleep.assert_called_once_with(5)
        mock_csv_manager_instance.append_row.assert_called_once_with(['lock_key', 'lock_value', 'Test message'])
        mock_lock_manager_instance.release_lock.assert_called_once()
        mock_sleep.assert_called_once_with(5)

    @patch('main.parse_arguments')
    @patch('main.CSVManager')
    @patch('main.LockManager')
    @patch('main.Redis')
    @patch('main.time.sleep')
    def test_main_lock_not_acquired(self, mock_sleep, mock_redis, mock_lock_manager, mock_csv_manager, mock_parse_arguments):
        # Mock the necessary objects and methods
        mock_args = MagicMock()
        mock_args.data = 'Test message'
        mock_args.sleep = 5
        mock_args.skip_release = False
        mock_parse_arguments.return_value = mock_args

        mock_redis_instance = MagicMock()
        mock_redis.from_url.return_value = mock_redis_instance

        mock_lock_manager_instance = MagicMock()
        mock_lock_manager.return_value = mock_lock_manager_instance
        mock_lock_manager_instance.acquire_lock.return_value = None

        mock_csv_manager_instance = MagicMock()
        mock_csv_manager.return_value = mock_csv_manager_instance

        # Call the main function
        main()

        # Assert that the expected methods were called with the correct arguments
        mock_parse_arguments.assert_called_once()
        mock_redis.from_url.assert_called_once_with('REDIS_CONN_STR')
        mock_lock_manager.assert_called_once_with('REDIS_CONN_STR')
        mock_csv_manager.assert_not_called()
        mock_lock_manager_instance.acquire_lock.assert_called_once()
        mock_sleep.assert_not_called()
        mock_csv_manager_instance.append_row.assert_not_called()
        mock_lock_manager_instance.release_lock.assert_not_called()
        mock_sleep.assert_not_called()

if __name__ == '__main__':
    unittest.main()