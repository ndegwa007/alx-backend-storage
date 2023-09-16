#!/usr/bin/env python3
"""module has a cache class"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """class creates a redis cache"""
    def __init__(self):
        """initialize cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """returns key to the data"""
        key = uuid.uuid4()
        uuid_str = str(key)
        self._redis.set(uuid_str, data)
        return uuid_str

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[int, str, None]:
        """gets key value in the right data format"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """convert to str"""
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int():
        """convert to int"""
        return self.get(key, fn=lambda d: int(d))
