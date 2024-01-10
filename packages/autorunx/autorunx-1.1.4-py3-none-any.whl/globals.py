# global

from importlib import import_module
import sys
import os
# or all platform. On window platform, sys.path[0] is same with basedir below:
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir)
sys.path.append(os.path.join(sys.path[0], 'lib/dataio'))
sys.path.append(os.path.join(sys.path[0], 'lib/dataprocess'))
sys.path.append(os.path.join(sys.path[0], 'lib/flowcontrol'))
sys.path.append(os.path.join(sys.path[0], 'lib/flowfunction'))
sys.path.append(os.path.join(sys.path[0], 'lib/eventreceive'))
sys.path.append(os.path.join(sys.path[0], 'lib/eventtransmit'))
sys.path.append(os.path.join(sys.path[0], '/system'))


# ====================================== global environment ======================================

ENV_WORK_DIR = os.getcwd()


def init_global_env(**kwargs):
    global ENV_WORK_DIR
    if 'ENV_WORK_DIR' in kwargs:
        ENV_WORK_DIR = kwargs['ENV_WORK_DIR']


# ====================================== data_center module ======================================

# data center
data_center = None


def init_data_center(**kwargs):
    global data_center
    DATA_CENTER_MODULE_NAME = "system.data_center"
    data_center = import_module(DATA_CENTER_MODULE_NAME)
    data_center.init(**kwargs)


# ====================================== node_center module ======================================


# node center
node_center = None


def init_node_center(**kwargs):
    global node_center
    NODE_CENTER_MODULE_NAME = "system.node_center"
    node_center = import_module(NODE_CENTER_MODULE_NAME)
    node_center.init(**kwargs)


# ====================================== log module ======================================


# log module
log_module = None
common_log = None
log = None


def init_log(**kwargs):
    """log module"""
    # get config and ini constant
    # global COMMON_LOG_FILE,LOG_FILE,LOG_MODULE_NAME
    LOG_MODULE_NAME = "system.log"
    # import module
    global log_module
    log_module = import_module(LOG_MODULE_NAME)
    # ini module
    log_module.init(**kwargs)
    # ini module function
    global common_log, log
    common_log = log_module.common_log
    log = log_module.log


# ====================================== aop module ======================================


# aop module
aop_module = None
aop = None


def init_aop(**kwargs):
    """aop module"""
    # get config and ini constant
    # global AOP_LOG_FILE,AOP_MODULE_NAME
    AOP_MODULE_NAME = "system.aop"
    # import module
    global aop_module
    aop_module = import_module(AOP_MODULE_NAME)
    # ini module
    aop_module.init(**kwargs)
    # ini module function
    global aop
    aop = aop_module.aop


# ====================================== engine module ======================================


# engine
engine = None


def init_engine(**kwargs):
    global engine
    ENGINE_MODULE_NAME = "system.engine"
    engine = import_module(ENGINE_MODULE_NAME)
    # params: graph:{node_list:[],edge_list:[]}
    engine.init(**kwargs)


# ====================================== init & start ======================================


def init(**kwargs):
    # print(kwargs)
    if "system" in kwargs and "global" in kwargs["system"]:
        init_global_env(**kwargs["system"]["global"])
    if "system" in kwargs and "data_center" in kwargs["system"]:
        init_data_center(**kwargs["system"]["data_center"])
    else:
        init_data_center()
    if "system" in kwargs and "node_center" in kwargs["system"]:
        init_node_center(**kwargs["system"]["node_center"])
    else:
        init_node_center()
    if "system" in kwargs and "aop" in kwargs["system"]:
        init_aop(**kwargs["system"]["aop"])
    else:
        init_aop()
    if "system" in kwargs and "log" in kwargs["system"]:
        init_log(**kwargs["system"]["log"])
    else:
        init_log()
    if "graph" in kwargs:
        init_engine(**kwargs["graph"])
    else:
        print("Error: Invalid profile!")


def start():
    engine.start()
