
import sys
import os
import globals
from threading import Lock

import copy

"""
key: data id
value: data value
"""
data_dict = {}
data_dict_lock = Lock()


def init(**kwargs):
    pass


def put(key, value, **kwargs):
    with data_dict_lock:
        data_dict[key] = copy.deepcopy(value)


def get(key, **kwargs):
    ret = None
    with data_dict_lock:
        ret = copy.deepcopy(data_dict[key])
    return ret


def get_dict_by_prefix(key, **kwargs):
    tmp_dict = {}
    with data_dict_lock:
        for k in data_dict:
            if str(k).startswith(key):
                tmp_dict[k] = copy.deepcopy(data_dict[k])
    return tmp_dict


def has(key, **kwargs):
    ret = False
    with data_dict_lock:
        ret = key in data_dict
    return ret
