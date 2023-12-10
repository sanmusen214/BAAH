import subprocess
import sys
import os
import logging
from typing import Tuple

logging.getLogger("subprocess").setLevel(logging.WARNING)

def subprocess_run(cmd: Tuple[str], isasync=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding = "utf-8"):
    """
    Run a command in a subprocess and return the instance.
    
    Parameters
    ==========
    cmd: list
        The command to run.
        
    Returns
    =======
    pipeline
    """
    if isasync:
        # 异步非阻塞执行
        return subprocess.Popen(cmd, stdout=stdout, stderr=stderr, encoding=encoding)
    else:
        # 同步阻塞执行
        return subprocess.run(cmd, stdout=stdout, stderr=stderr, encoding=encoding)
    
    