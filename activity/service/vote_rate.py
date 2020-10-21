from threading import Lock
import logging


class VoteRate:

    def __init__(self):
        self.lock = Lock()
        self._next_rates = {}
        self._rates = {1.0: 0.5, 0.5: 0.25, 0.25: 0.25}

    def next_rate(self, user_id: int):
        self.lock.acquire()
        try:
            rate = self._next_rates.get(user_id, 1.0)
            self._next_rates[user_id] = self._rates[rate]
            logging.getLogger().info(
                f"vote_rate.py --- user_id: {user_id} rate: {rate} next_rate: {self._rates[rate]}")
            return rate
        finally:
            self.lock.release()
