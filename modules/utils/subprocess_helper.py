import subprocess
import sys
import os
import logging
from typing import Tuple

logging.getLogger("subprocess").setLevel(logging.WARNING)

def subprocess_run(cmd: Tuple[str]|str, isasync=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding = "utf-8", shell=False):
    """
    Run a command in a subprocess and return the instance.
    
    Parameters
    ==========
    cmd: list|str
        The command to run.
        
    Returns
    =======
    pipeline
    """
    # https://www.cnblogs.com/superbaby11/p/16195273.html
    # shell 为True时，cmd可以是字符串，否则是列表。列表的第一个元素是命令，后面的元素是传递给shell1的参数。
    if isasync:
        # 异步非阻塞执行
        return subprocess.Popen(cmd, stdout=stdout, stderr=stderr, encoding=encoding, shell=shell)
    else:
        # 同步阻塞执行
        return subprocess.run(cmd, stdout=stdout, stderr=stderr, encoding=encoding, shell=shell)
    
    