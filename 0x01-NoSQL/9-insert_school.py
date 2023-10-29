#!/usr/bin/python3
"""insert a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """new document"""

    doc = dict(kwargs)
    return mongo_collection.insert_one(doc).inserted_id
