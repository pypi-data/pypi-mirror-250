import globals
from threading import Thread


g_is_started=False
g_is_finished=False


def is_started():
    return g_is_started


def is_finished():
    return g_is_finished


def event_run(**kwargs):
    global g_is_started,g_is_finished
    g_is_started=True
    node_config=kwargs["_config"]
    if "nxt_edge_id" not in node_config or len(node_config["nxt_edge_id"])<=0:
        return
    edge_id=node_config["nxt_edge_id"][0]
    if edge_id in globals.engine.edges_config:
        globals.engine.handle_flow_node(globals.engine.edges_config[edge_id]["nxt_id"])
    g_is_finished=True
    return {}


def run(**kwargs):
    t=Thread(target=event_run,kwargs=kwargs)
    t.start()

