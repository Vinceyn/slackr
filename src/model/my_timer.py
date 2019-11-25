''' Timer function spawns a new thread
that executes the supplied at the end of the timer'''
import datetime
import threading

def my_timer(time, execute_function, function_args):
    '''Executes function after time has been reached, time a datetime
    for when when it the function executes, function_args is a tuple
    of args passed in'''
    now = datetime.datetime.now()
    sleep_time = (time-now).total_seconds()
    if sleep_time < 0:
        raise ValueError
    threading.Timer(sleep_time, execute_function, function_args).start()
