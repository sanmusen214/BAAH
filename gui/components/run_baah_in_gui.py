import subprocess
import time
import subprocess
import threading
import queue
from nicegui import ui, run

# 显示命令行输出的地方

def run_baah_task(msg_obj, output_area, config):

    # 启动子进程并执行命令行程序
    # cd D:\myCode\PYTHON_file\碧蓝档案自动每日\BAAH1.2.0\BAAH.exe
    # BAAH.exe 国际服.json
    # command = [r"D:\myCode\PYTHON_file\碧蓝档案自动每日\BAAH1.2.0\BAAH.exe", "国际服.json"]

    # D://myCode\PYTHON_file\碧蓝档案自动每日\BAAH1.2.0

    def enqueue_output(pipe, queue):
        try:
            for line in iter(pipe.readline, ''):
                queue.put(line)
            pipe.close()
        except Exception as e:
            print(e)

    # 定义运行程序的命令和参数
    # 运行BAAH_main()方法
    command = ["BAAH.exe", config.nowuserconfigname]
    print("RUN")
    msg_obj["msg"] = "<br>" + f"{config.nowuserconfigname}" + "<br>" + msg_obj["msg"]
    output_area.refresh()
    # 使用subprocess.Popen来运行外部程序
    with subprocess.Popen(command, stdout=subprocess.PIPE, text=True, bufsize=1) as process:
        # 创建队列来保存子进程输出
        stdout_queue = queue.Queue()

        # 启动线程来读取子进程的标准输出
        stdout_thread = threading.Thread(target=enqueue_output, args=(process.stdout, stdout_queue))
        stdout_thread.daemon = True
        stdout_thread.start()

        try:
            while True:
                # 尝试从stdout_queue中获取数据
                try:
                    output = stdout_queue.get_nowait()
                except queue.Empty:
                    output = None

                if output:
                    msg_obj["msg"] = output + "<br>" + msg_obj.get("msg", "")
                    output_area.refresh()
                    
                # 检查子进程是否已经结束
                if process.poll() is not None:
                    break
                
                # 检查是否要求信号中断，或者子进程输出有GUI_BAAH_TASK_END关键字
                if msg_obj["stop_signal"] == 1 or (isinstance(output, str) and "GUI_BAAH_TASK_END" in output):
                    msg_obj["stop_signal"] = 0
                    msg_obj["runing_signal"] = 0.25
                    # shut down the process
                    process.terminate()
                    process.wait()
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Terminating the process...")
            process.terminate()
            process.wait()
    msg_obj["runing_signal"] = 0
    print("Process finished.")
    msg_obj["msg"] = "<br>" + f"{config.nowuserconfigname}" + "<br>" + msg_obj["msg"]
    output_area.refresh()