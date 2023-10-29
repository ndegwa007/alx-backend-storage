#!/usr/bin/python3 
"""update documents by filter record in a collection"""


def update_topics(mongo_collection, name, topics):
    """update documents depending on name"""
    return mongo_collection.update_many({'name': name}, {'$set':  {'topics': topics}})
