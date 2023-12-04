import subprocess
import sys
import os
import logging
from typing import Tuple

logging.getLogger("subprocess").setLevel(logging.WARNING)

def subprocess_run(cmd: Tuple[str], isasync=False) -> bool:
    """
    Run a command in a subprocess and return the return code.
    
    Parameters
    ==========
    cmd: list
        The command to run.
        
    Returns
    =======
    bool
        True if the command returns 0, False otherwise.
    """
    if isasync:
        # 异步非阻塞执行
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    else:
        # 同步阻塞执行
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    
    # if p.returncode == 0:
    #     logging.info(f"Executing {cmd}...OK")
    # else:
    #     logging.info(f"Executing {cmd}...Failed")
    return p.returncode == 0