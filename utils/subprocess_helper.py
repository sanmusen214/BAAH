import subprocess
import sys
import os
import logging

type Cmd = list[str]

logging.getLogger("subprocess").setLevel(logging.WARNING)

def subprocess_run(cmd: Cmd) -> bool:
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
    p = subprocess.run(cmd, encoding="utf-8")
    if p.returncode == 0:
        logging.info(f"Executing {cmd}...OK")
    else:
        logging.info(f"Executing {cmd}...Failed")
    return p.returncode == 0