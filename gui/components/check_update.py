from ..define import gui_shared_config

from nicegui import ui, run
import time
import requests
import os
from datetime import datetime
from update import whether_has_new_version

g_result = None
g_datetime = ""

async def only_check_version():
    global g_result, g_datetime
    datetime_now = datetime.now().strftime("%Y-%m-%d %H")
    # 缓存判断日期，如果日期相同就不用再次请求
    if datetime_now == g_datetime:
        print(f"Use cached release info: {datetime_now}")
        return g_result
    # ==请求最新版本信息==
    g_result = whether_has_new_version()
    # ==================
    g_datetime = datetime_now # 更新缓存判断值
    return g_result
