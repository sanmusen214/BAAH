import multiprocessing
import multiprocessing.managers
from BAAH import BAAH_core_process, BAAH_single_func_process

class RunningBAAHProcess:
    def __init__(self):
        self.__ctx = multiprocessing.get_context("spawn")
        self.__name2process:dict[str, multiprocessing.Process] = dict()
        self.__name2queue:dict[str, multiprocessing.Queue] = dict()
        self.__name2manager:dict[str, multiprocessing.managers.SyncManager] = dict()
        self.__name2status:dict[str, dict] = dict()
    
    def get_status_obj(self, configname):
        if configname not in self.__name2status:
            self.__name2status[configname] = {
                "runing_signal": 0,
                "now_logArea_id": 0 # 当前聚焦的日志窗口id，当新的窗口打开时，旧的窗口的监听日志的while循环会break
            }
        return self.__name2status[configname]

    def check_is_running(self, configname):
        process = self.get_process(configname)
        if not process:
            return False
        return process.is_alive()
    
    def get_process(self, configname):
        return self.__name2process.get(configname, None)

    def get_queue(self, configname):
        return self.__name2queue.get(configname, None)
    
    def get_manager(self, configname):
        return self.__name2manager.get(configname, None)
    
    def _start_task(self, configname, target_func, input_kwargs, pass_queue_name = None):
        """
        启动目标进程，返回queue

        如果进程已经在运行，则返回原有的queue
        """
        if not self.check_is_running(configname):
            # 用于共享消息
            manager = self.__ctx.Manager()
            queue = manager.Queue()
            self.__name2manager[configname] = manager
            self.__name2queue[configname] = queue
            # 解构传入的参数，加入queue，queue对应的key为${pass_queue_name}
            if pass_queue_name:
                input_kwargs[pass_queue_name] = queue
            # 启动进程
            p = self.__ctx.Process(target=target_func, kwargs=input_kwargs,
            daemon=True)
            self.__name2process[configname] = p
            p.start()
            # 更新status
            this_status = self.get_status_obj(configname)
            this_status["runing_signal"] = 1

        return self.__name2queue[configname]

    def run_task(self, configname):
        return self._start_task(configname, BAAH_core_process, {
            "reread_config_name": configname,
            "must_auto_quit": True
            },
            pass_queue_name="msg_queue"
        )
    
    def run_specific_task(self, configname, torunfunc_configname):
        return self._start_task(configname, BAAH_single_func_process, {
            "reread_config_name": configname,
            "to_run_func_config_name": torunfunc_configname
        }, pass_queue_name = "msg_queue")
        
    def stop_task(self, configname, logArea = None):
        """terminate process and do side effect"""
        def multiprint(sen):
            logArea and logArea.push(sen)
            print(sen)
        
        if self.check_is_running(configname):
            # close process
            multiprint(f"terminating {configname}...")
            try:
                process = self.__name2process[configname]
                if process.is_alive():
                    process.terminate()
            except Exception as e:
                print(f"Error when terminate process of {configname}: {e}")

        # stop task副作用，清空queue，关掉manager，修改状态量

        # clear queue
        multiprint("clearing queue...")
        try:
            queue = self.get_queue(configname)
            # 输出queue中剩余的信息
            while(not queue.empty()):
                output = queue.get_nowait()
                logArea and logArea.push(output)
        except BrokenPipeError as bpe:
            print(f"broken pipe: {bpe}")
        except Exception as e:
            print(f"Exception when clear pipe: {e}")
        # close queue/manager
        multiprint("closing queue/manager...")
        try:
            manager = self.get_manager(configname)
            manager.shutdown()
        except Exception as e:
            print(f"Error when close queue (manager) of {configname}: {e}")
        # 更新status/按钮状态
        msg_obj = self.get_status_obj(configname)
        msg_obj["runing_signal"] = 0
        multiprint(f"side effect of stopping {configname} done")
        
        
RunningBAAHProcess_instance = RunningBAAHProcess()