#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

transactions = [
    {
        'id': 1,
        'sum': 10,
        'source_id': 2,
        'destination_id': 3,
        'date': '2017/08/21 23:07:33'
    },
    {
        'id': 2,
        'sum': 30,
        'source_id': 1,
        'destination_id': 2,
        'datetime': '2017/08/20 23:07:33'
    }
]


def get(id=False,account_id=False):
    if id:
        for item in transactions:
            if item['id']==id:
                return item
    if account_id:
        result=[]
        for item in transactions:
            if item['source_id']==account_id or item['destination_id']==account_id:
                result.append(item)
        return result
    if not id and not account_id:
        return transactions

def add(transaction):
    transactions.append(transaction)
    return True