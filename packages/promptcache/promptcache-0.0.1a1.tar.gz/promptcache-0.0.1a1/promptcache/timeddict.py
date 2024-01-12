import time
from threading import Lock


class TimedDict:
    """Untested - DONT USE"""

    def __init__(self, expiry_time):
        self.expiry_time = expiry_time
        self.dict = {}
        self.expiry_times = {}
        self.lock = Lock()

    def _cleanup(self):
        current_time = time.time()
        keys_to_delete = [
            key for key, expiry in self.expiry_times.items() if expiry < current_time]
        for key in keys_to_delete:
            del self.dict[key]
            del self.expiry_times[key]

    def __getitem__(self, key):
        with self.lock:
            self._cleanup()
            if key in self.dict:
                return self.dict[key]
            raise KeyError(key)

    def __setitem__(self, key, value):
        with self.lock:
            self._cleanup()
            self.dict[key] = value
            self.expiry_times[key] = time.time() + self.expiry_time

    def __delitem__(self, key):
        with self.lock:
            if key in self.dict:
                del self.dict[key]
                del self.expiry_times[key]
            else:
                raise KeyError(key)

    def __contains__(self, key):
        with self.lock:
            self._cleanup()
            return key in self.dict

    def __len__(self):
        with self.lock:
            self._cleanup()
            return len(self.dict)

    def __str__(self):
        with self.lock:
            self._cleanup()
            return str(self.dict)
