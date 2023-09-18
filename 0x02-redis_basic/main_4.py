#!/usr/bin/env python3
"""test history"""

Cache = __import__('exercise').Cache

cache = Cache()

cache.store("foo")
cache.store("bar")
cache.store(42)

print(cache.replay(cache.store))
