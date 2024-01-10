
import globals



def run(**kwargs):
    globals.log(msg="func test start...")
    params=""
    for k in kwargs:
        params="{}{}: {}".format("" if params=="" else params+", ",k,kwargs[k])
    globals.log(msg="params: { "+params+" }")
    globals.log(msg="func test end...")
    return {**kwargs}

























