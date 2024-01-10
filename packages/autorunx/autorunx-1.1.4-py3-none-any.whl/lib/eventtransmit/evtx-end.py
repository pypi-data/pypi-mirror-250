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
    g_is_finished=True
    globals.engine.stop()


def run(**kwargs):
    t=Thread(target=event_run,kwargs=kwargs)
    t.start()






















