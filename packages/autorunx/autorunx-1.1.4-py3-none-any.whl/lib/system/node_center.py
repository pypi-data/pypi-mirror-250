
import sys,os
import globals


"""
key: node id
value: node
"""
node_dict={}


def init(**kwargs):
    pass


def put(key,value,**kwargs):
    node_dict[key]=value


def get(key,**kwargs):
    return node_dict[key]


def has(key,**kwargs):
    return key in node_dict


def generate(key,**kwargs):
    """
    key: node_name, node's filename but bot include extension, module name
    """
    module=globals.import_module(key)
    return module


def get_or_generate(id,node_name,**kwargs):
    """
    id: node_id or node_name, typically this is the node_id
    node_name: node_name, node's filename but bot include extension, also called the module name
    """
    if id in node_dict:
        return node_dict[id]
    else:
        module=globals.import_module(node_name)
        return module










































