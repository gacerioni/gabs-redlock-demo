from pottery import Redlock
from redis import Redis


class LockManager:
    def __init__(self, redis_url, lock_key='csv_file_gabs', auto_release_time=30):
        self.redis = Redis.from_url(redis_url)
        self.lock = Redlock(key=lock_key, masters={self.redis}, auto_release_time=auto_release_time)

    def acquire_lock(self):
        return self.lock.acquire()

    def release_lock(self):
        return self.lock.release()
