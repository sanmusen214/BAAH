import time
from nicegui import ui, run
from .running_task_pool import RunningBAAHProcess_instance as taskpool

# 显示命令行输出的地方

def run_baah_task_and_bind_log(logArea, configname):
    msg_obj = taskpool.get_status_obj(configname)
    queue = taskpool.run_task(configname)
    process = taskpool.get_process(configname)
    # 防止新的日志输出线程和旧的日志输出线程争抢queue，每次调用此方法都会记录logArea_ID，存储在msg_obj中，如果id与本次ID不同则退出while，结束此线程
    logArea_ID = time.time()
    print(f"start log area thread id: {logArea_ID}")
    msg_obj["now_logArea_id"]=logArea_ID
    while(msg_obj["runing_signal"] == 1 and msg_obj["now_logArea_id"]==logArea_ID):
        try:
            output = queue.get_nowait()
        except:
            output = None
        if output:
            logArea.push(output)
        time.sleep(0.01)
    print(f"quit log area thread id: {logArea_ID}")

def stop_baah_task(logArea, configname):
    msg_obj = taskpool.get_status_obj(configname)
    taskpool.stop_task(configname)
    logArea.push(f"Stop: {configname}")
    print(f"Stop: {configname}")