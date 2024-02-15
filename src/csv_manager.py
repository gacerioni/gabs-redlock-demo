import csv
import os
import datetime
from redis import Redis


class CSVManager:
    def __init__(self, filename, redis_instance):
        self.filename = filename
        self.redis = redis_instance
        self.client_id_key = "gabs_client_id_counter"  # Redis key for the incremental client ID

    def get_next_client_id(self):
        # Increment and retrieve the next client ID from Redis
        next_id = self.redis.incr(self.client_id_key)
        return next_id

    def append_row(self, data, action_type="update", lock_token="N/A"):
        # Generate a timestamp for when the data is being appended
        timestamp = datetime.datetime.utcnow().isoformat()
        # Get the next incremental client ID from Redis
        client_id = self.get_next_client_id()
        # Prepare the row data with additional metadata
        row_data = [timestamp, client_id, lock_token, action_type, data]

        # Check if the file exists to determine if headers need to be written
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write headers if the file did not exist prior to this operation
            if not file_exists:
                writer.writerow(['Timestamp', 'ClientID', 'LockToken', 'ActionType', 'Data'])
            writer.writerow(row_data)
