import os
import argparse
import time
from dotenv import load_dotenv
from src.lock_manager import LockManager
from src.csv_manager import CSVManager
from src.logger_config import setup_logger

logger = setup_logger()

# CONSTANTS BY GABS THE NERDOLA
REDIS_CONN_STR = os.getenv('REDIS_CONN_STR', 'redis://default:password@localhost:6379/0')
REDIS_CSV_FILE_NAME = os.getenv('REDIS_CSV_FILE_NAME', '/tmp/output.csv')

# Load environment variables from .env file
load_dotenv()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Append data to a CSV file with distributed locking.')
    parser.add_argument('--data', type=str, help='Data to append to the CSV file', required=True)
    parser.add_argument('--sleep', type=int, default=0, help='Time in seconds to sleep before writing to the CSV file')
    parser.add_argument('--skip-release', action='store_true',
                        help='Skip releasing the lock to simulate a crash or stall')
    return parser.parse_args()


def main():
    args = parse_arguments()
    message = args.data  # Data from command-line argument
    sleep_time = args.sleep  # Time to sleep before writing to the CSV
    skip_release = args.skip_release  # Whether to skip releasing the lock

    lock_manager = LockManager(REDIS_CONN_STR)
    csv_manager = CSVManager(REDIS_CSV_FILE_NAME)

    if lock_manager.acquire_lock():
        try:
            logger.info('Lock acquired, appending to CSV after a delay.')
            if sleep_time > 0:
                logger.info(f'Sleeping for {sleep_time} seconds to simulate a long-running task.')
                time.sleep(sleep_time)  # Sleep for the specified amount of time
            csv_manager.append_row(['Data1', message])  # Customize as needed
        except Exception as e:
            logger.error(f'Error appending to CSV: {e}')
        finally:
            if not skip_release:
                lock_manager.release_lock()
                logger.info('Lock released.')
            else:
                logger.info('Simulating a crash/stall. Lock not released.')
    else:
        logger.info('Failed to acquire lock.')


if __name__ == '__main__':
    main()
