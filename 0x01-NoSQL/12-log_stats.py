#!/usr/bin/env python3
"""count the number of documents in nginx collection"""
from pymongo import MongoClient


def logs_count():
    """start a pymongo client and get stats"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    get_count = nginx_collection.count_documents({'method': 'GET'})
    post_count = nginx_collection.count_documents({'method': 'POST'})
    put_count = nginx_collection.count_documents({'method': 'PUT'})
    patch_count = nginx_collection.count_documents({'method': 'PATCH'})
    delete_count = nginx_collection.count_documents({'method': 'DELETE'})
    total_count = nginx_collection.count_documents({})

    status_count = nginx_collection.count_documents({'path': '/status'})
    return f"{total_count} logs \n Methods:\n\
{' ':>5}method GET: {get_count} \n\
{' ':>5}method POST: {post_count} \n\
{' ':>5}method PUT: {put_count} \n\
{' ':>5}method PATCH: {patch_count} \n\
{' ':>5}method DELETE: {delete_count} \n\
{status_count} status check"


if __name__ == '__main__':
    print(logs_count())
