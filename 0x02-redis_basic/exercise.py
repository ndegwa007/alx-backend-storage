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

    def replay(self, method: Callable) -> str:
        """display history of calls"""
        method_name = "Cache." + method.__name__
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        input_history = self._redis.lrange(input_key, 0, -1)
        output_history = self._redis.lrange(output_key, 0, -1)
        call_times = len(input_history)
        call_string = []
        for input_data, output_key in zip(input_history, output_history):
            input_data = input_data.decode('utf-8')
            output_key = output_key.decode('utf-8')
            call_string.append(f"{method_name}(*{input_data}) -> {output_key}")
        replay_str = f"{method_name} was called {call_times} times:\n"
        replay_str += "\n".join(call_string)
        return replay_str
