from pottery import Redlock
from redis import Redis

# GABS CONSTANTS, BECAUSE I AM NOT SURE I WANT TO EXPOSE THESE CONFIGs YET.
GABS_LOCK_KEY = 'csv_file_gabs'
#GABS_FULL_LOCK_KEY = f'redlock:{GABS_LOCK_KEY}'
GABS_WAIT_TIME = 30


class LockManager:
    def __init__(self, redis_url, lock_key=GABS_LOCK_KEY, auto_release_time=GABS_WAIT_TIME):
        self.redis = Redis.from_url(redis_url)
        # Store the full lock key including the Redlock prefix
        self.full_lock_key = f'redlock:{lock_key}'
        self.lock = Redlock(key=lock_key, masters={self.redis}, auto_release_time=auto_release_time)

    def acquire_lock(self):
        # Attempt to acquire the lock and return the full lock key as the "token" if successful
        if self.lock.acquire():
            lock_value = self.redis.get(self.full_lock_key)
            return self.full_lock_key, lock_value
        return None, None

    def release_lock(self):
        # Release the lock
        return self.lock.release()
