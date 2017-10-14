#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

accounts = [
    {
        'id': 1,
        'balance': 100000,
        'owner_id': 1
    },
    {
        'id': 2,
        'balance': 1000,
        'owner_id': 2
    },
    {
        'id': 3,
        'balance': 0,
        'owner_id': 3
    },
]


def get(id=False):
    if id:
        for item in accounts:
            if item['id']==id:
                return item
    else:
        return accounts