
import sys,os
import globals
import copy


def run(**kwargs):
    # print("control queue...")
    node_config=kwargs["_config"]
    if "nxt_edge_id" not in node_config:
        return
    for edge_id in node_config["nxt_edge_id"]:
        if edge_id in globals.engine.edges_config:
            globals.engine.handle_flow_node(globals.engine.edges_config[edge_id]["nxt_id"])
    return {}





















