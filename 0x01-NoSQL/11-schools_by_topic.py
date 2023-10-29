#!/usr/bin/python3
"""filter by topics in school documents"""


def schools_by_topic(mongo_collection, topic):
    """get school name"""
    return mongo_collection.find({'topics': {'$in': [topic]}})
