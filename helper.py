'''
Misc helper func and class
'''
from subprocess import CompletedProcess, SubprocessError, run
import time
import math
from config import Config

line_feed = '\n'

def round_by(num: float, cutnum: float) -> int:
    '''
    round the float number up if the decimal part is larger than cutnum
    otherwise round down
    '''
    dec_part, int_part = math.modf(num)
    if dec_part > cutnum:
        int_part += 1
    return int(int_part)

def get_localtime(time_stamp=None):
    if time_stamp is None:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))

def run_cmd(cmd, try_time=1, wait_time=3, timeout=120) -> CompletedProcess:
    '''
    try running the info cmd {try_time} times and wait {wait_time} between each run if subprocessexceptions are raised.
    default be 1 run.
    along with common run() settings (including exception handling)
    # TODO(shaoqz): should use this as general function to run commands in local shell.
    '''
    for i in range(try_time):
        try:
            this_run = run(cmd, timeout=timeout, check=True,  text=True, shell=True, capture_output=True)
        except SubprocessError as e:
            if Config.debug > 0:
                print(f'Error running {cmd}: {repr(e)}')
                print(f'    stderr: {str(e.stderr).strip()}')
                print(f'    stdout: {str(e.stdout).strip()}')
                print(f'trying again... ({i+1}/{try_time})')
        else: # untill there's no error
            if Config.debug > 0:
                if i > 0:
                    print(f'finished {cmd} after {i+1} tries @{get_localtime()}')
            return this_run
        # wait before next try
        time.sleep(wait_time)
    # exceed the try time
    raise SubprocessError(f'Failed running `{cmd}` after {try_time} tries @{get_localtime()}')
    # TODO change to a custom error
