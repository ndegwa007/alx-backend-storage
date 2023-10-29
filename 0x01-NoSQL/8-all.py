#!/usr/bin/env python3
"""script list all the documents in a collection"""


def list_all(mongo_collection):
    """get the list of all documents"""
    if mongo_collection.find() == []:
        return []

    return mongo_collection.find()
