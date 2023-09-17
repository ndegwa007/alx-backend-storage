#!/usr/bin/env python3
"""module has a cache class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """decorator for method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """inner wrapper func"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string in Redis
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        result = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def count_calls(fn: Callable) -> Callable:
    """calls the method it wraps"""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        """wraps logic to the method"""
        key = fn.__qualname__
        result = self._redis.incr(key)
        self._redis.set(key, result)
        return fn(self, *args, **kwargs)
    return wrapper


class Cache:
    """class creates a redis cache"""
    def __init__(self):
        """initialize cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def get_int(key: str) -> int:
        """convert to int"""
        return self.get(key, fn=lambda d: int(d))
