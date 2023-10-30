#!/usr/bin/env python3
"""count the number of documents in nginx collection"""
from pymongo import MongoClient


def logs_count(collection):
    """start a pymongo client and get stats"""

    print("{} logs".format(collection.count_documents({})))
    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in http_methods:
        print("method {}: {}".format(
            method,
            collection.count_documents({'method': method}))
            )
    print("{} status check".format(
        collection.count_documents({'path': '/status'}))
        )


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    nginx_collection = client.logs.nginx
    logs_count(nginx_collection)
