# Distributed Locking with Redis and Python

This project demonstrates the implementation of distributed locking using Redis and Python. It showcases how to manage access to shared resources (in this case, a CSV file) in a distributed environment to prevent race conditions and ensure data consistency.

## Features

- **Distributed Locking**: Utilizes Redis to create distributed locks.
- **Flexible Configuration**: Supports configuration through environment variables.
- **Command Line Interface**: Offers command-line options to customize the execution, including simulating long-running tasks and crash/stall scenarios.

## Getting Started

### Prerequisites

- Python 3.6+
- Redis server
- `python-dotenv` and `redis` Python packages

### Installation

1. Clone the repository:

   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

YOU MAY USE A .env FILE AT THE ROOT OF YOUR REPO:

```
REDIS_CONN_STR="redis://default:q7bx@redis-212121.2121.us-east-1-4.ec2.cloud.redislabs.com:424242/0"
REDIS_CSV_FILE_NAME="/tmp/gabs.csv"
```

- `REDIS_CONN_STR`: The connection string for your Redis instance.
- `REDIS_CSV_FILE_NAME`: The path to the CSV file to which data will be appended.

### Usage

Run the script with the following command:

```bash
python main.py --data "Your data here" [--sleep <seconds>] [--skip-release]
```

- `--data`: The data to append to the CSV file.
- `--sleep`: (Optional) Time in seconds to sleep before writing to the CSV file, simulating a long-running task.
- `--skip-release`: (Optional) Skip releasing the lock to simulate a crash or stall scenario.

### Example

To append data to the CSV file with a 5-second delay:

```bash
python main.py --data "Example data" --sleep 5
```

To simulate a scenario where the client crashes before releasing the lock:

```bash
python main.py --data "Test data" --skip-release
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

Distributed under the MIT License. See `LICENSE` for more information.
