from nicegui import ui
import json
from modules.utils.MyConfig import MyConfigger
from modules.AllTask.myAllTask import task_dict

@ui.refreshable
def show_GUI(load_jsonname):
    
    with ui.row():
        ui.label("Blue Archive Aris Helper").style('font-size: xx-large')
    
    config = MyConfigger(load_jsonname)
    # 在GUI里，我们只使用config.configdict这个字典，不用config下的属性
    all_list_key_names = [
        "TIMETABLE_TASK",
        "WANTED_HIGHEST_LEVEL",
        "SPECIAL_HIGHTEST_LEVEL",
        "EXCHANGE_HIGHEST_LEVEL",
        "EVENT_QUEST_LEVEL",
        "HARD",
        "NORMAL",
        "TASK_ORDER",
    ]
    
    all_str_key_names = [
        "TARGET_EMULATOR_PATH",
        "PIC_PATH",
        "ACTIVITY_PATH",
        "ADB_PATH",
        "SCREENSHOT_NAME",
    ]
    
    all_num_key_names = [
        "TARGET_PORT",
        "TIME_AFTER_CLICK",
    ]
    # 不在configdict中的key，添加默认值
    for key in all_list_key_names:
        if key not in config.configdict:
            if key == "TASK_ORDER":
                config.configdict[key] = ["登录游戏"]
            else:
                config.configdict[key] = []
    for key in all_str_key_names:
        if key not in config.configdict:
            if key == "ADB_PATH":
                config.configdict[key] = "./tools/adb/adb.exe"
            elif key == "SCREENSHOT_NAME":
                config.configdict[key] = "screenshot.png"
            else:
                config.configdict[key] = ""
    for key in all_num_key_names:
        if key not in config.configdict:
            config.configdict[key] = 1

    all_task_names = list(task_dict.keys())
    
    server_map = {
        "server2pic": {
            "日服":"./assets_jp",
            "国际服":"./assets",
        },
        "pic2server": {
            "./assets_jp":"日服",
            "./assets":"国际服",
        },
        "server2activity": {
            "日服":"com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
            "国际服":"com.nexon.bluearchive/.MxUnityPlayerActivity",
        },
        "activity2server": {
            "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity":"日服",
            "com.nexon.bluearchive/.MxUnityPlayerActivity":"国际服",
        }
    }
    
    # =============================================
    
    def list_edit_area(datadict, linedesc):
        """
        keyname: configdict中的key
        linedesc: 描述列表，长度代表列表维度
            [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
        """
        dim = len(linedesc)
        subdim = 0
        if dim == 3:
            subdim = len(linedesc[2])
        @ui.refreshable
        def item_list():
            for i in range(len(datadict)):
                line_item = datadict[i]
                ui.label(f'第{i+1}{linedesc[0]}: (-1次即为max次，-2次即为max-2次)')
                with ui.row():
                    for j in range(len(line_item)):
                        if len(linedesc) == 2:
                            # 第几个教室
                            ui.number(f'{linedesc[1]}',
                                        min=1,
                                        step=1,
                                        precision=0,
                                        format="%.0f",
                                        value=line_item[j],
                                        on_change=lambda v,i=i,j=j: datadict[i].__setitem__(j, int(v.value)),
                                        ).style('width: 100px')
                        elif len(linedesc) == 3:
                            ui.label(f'{linedesc[1]}:')
                            with ui.row():
                                with ui.card():
                                    for k in range(len(line_item[j])):
                                        #  遍历关卡和次数
                                        min_value = 1
                                        if k == subdim-1:
                                            min_value = -99
                                        ui.number(f'{linedesc[2][k]}',
                                                    min=min_value,
                                                    step=1,
                                                    precision=0,
                                                    format="%.0f",
                                                    value=line_item[j][k],
                                                    on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                    ).style('width: 100px')
                                
                    with ui.column():
                        ui.button(f"添加{linedesc[1]}", on_click=lambda i=i: add_item_item(i))
                        if len(datadict[i]) > 0:
                            ui.button(f"删除{linedesc[1]}", on_click=lambda i=i: del_item_item(i), color="red")
            with ui.row():
                ui.button(f"添加{linedesc[0]}", on_click=add_item)
                if len(datadict) > 0:
                    ui.button(f"删除{linedesc[0]}", on_click=del_item, color="red")
        
        def add_item():
            datadict.append([])
            item_list.refresh()
        
        def del_item():
            datadict.pop()
            item_list.refresh()
        
        def add_item_item(item_ind):
            if dim == 2:
                datadict[item_ind].append(1)
            elif dim == 3:
                if subdim == 2:
                    datadict[item_ind].append([1, 1])
                elif subdim == 3:
                    datadict[item_ind].append([1, 1, 1])
                
            item_list.refresh()
        
        def del_item_item(item_ind):
            datadict[item_ind].pop()
            item_list.refresh()

        item_list()
    
    # =============================================

    with ui.row().style('min-width: 800px;'):
        with ui.column().style('width: 10vw; overflow: auto; position: sticky; top: 20px; min-width: 150px;'):
            with ui.card():
                ui.link('模拟器配置', '#EMULATOR')
                ui.link('服务器配置', '#SERVER')
                ui.link('任务执行顺序', '#TASK_ORDER')
                ui.link('后续配置文件', '#NEXT_CONFIG')
                ui.link('课程表', '#COURSE_TABLE')
                ui.link('悬赏通缉', '#WANTED')
                ui.link('特殊任务', '#SPECIAL_TASK')
                ui.link('学园交流会', '#EXCHANGE')
                ui.link('活动关卡', '#ACTIVITY')
                ui.link('困难关卡', '#HARD')
                ui.link('普通关卡', '#NORMAL')
                ui.link('其他设置', '#TOOL_PATH')


        with ui.column().style('width: 80vw; overflow: auto; min-width: 450px;'):
            with ui.row():
                ui.link_target("EMULATOR")
                ui.label('模拟器配置').style('font-size: x-large')
                
            with ui.row():
                ui.number('模拟器端口',
                        step=1,
                        precision=0,
                        ).bind_value(config.configdict, 'TARGET_PORT', forward=lambda v: int(v)).style('width: 400px')
            with ui.row():    
                ui.input('模拟器路径'
                         ).bind_value(config.configdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')

            with ui.row():
                ui.link_target("SERVER")
                ui.label('服务器配置').style('font-size: x-large')
            
            server = ui.radio(["日服", "国际服"], value=server_map["activity2server"][config.configdict['ACTIVITY_PATH']], on_change=lambda a:set_server_info(a.value)).props('inline')
            
            def set_server_info(server):
                config.configdict["PIC_PATH"] = server_map["server2pic"][server]
                config.configdict["ACTIVITY_PATH"] = server_map["server2activity"][server]
                
            
            # with ui.row():
            #     ui.input('匹配模板图片路径').bind_value(config.configdict, 'PIC_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
                
            # with ui.row():
            #     ui.input('游戏包名').bind_value(config.configdict, 'ACTIVITY_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.link_target("TASK_ORDER")
                ui.label('任务执行顺序').style('font-size: x-large')
                
            @ui.refreshable
            def task_order():
                for i in range(len(config.configdict["TASK_ORDER"])):
                    with ui.row():
                        ui.label(f'第{i+1}个任务:')
                        atask = ui.select(all_task_names,
                                  value=config.configdict["TASK_ORDER"][i],
                                  on_change=lambda v,i=i: config.configdict["TASK_ORDER"].__setitem__(i, v.value),
                                  )
                        if i==0:
                            atask.set_enabled(False)
                        ui.button("添加任务", on_click=lambda i=i+1: add_task(i))
                        if len(config.configdict["TASK_ORDER"]) > 0 and i > 0:
                            ui.button("删除任务", on_click=lambda i=i: del_task(i), color="red")

            def add_task(i):
                config.configdict["TASK_ORDER"].insert(i, "邮件")
                task_order.refresh()
            
            def del_task(i):
                config.configdict["TASK_ORDER"].pop(i)
                task_order.refresh()
            
            task_order()
            
            with ui.row():
                ui.link_target("NEXT_CONFIG")
                ui.label('后续配置文件').style('font-size: x-large')
                
            ui.input('执行完此配置文件过后，继续执行配置文件').bind_value(config.configdict, 'NEXT_CONFIG',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.link_target("COURSE_TABLE")
                ui.label('课程表').style('font-size: x-large')
            
            list_edit_area(config.configdict["TIMETABLE_TASK"], ["个地区", "教室"])
                
            
            with ui.row():
                ui.link_target("WANTED")
                ui.label('悬赏通缉').style('font-size: x-large')
            
            list_edit_area(config.configdict["WANTED_HIGHEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]])
            
            with ui.row():
                ui.link_target("SPECIAL_TASK")
                ui.label('特殊任务').style('font-size: x-large')
                
            list_edit_area(config.configdict["SPECIAL_HIGHTEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]])
            
            with ui.row():
                ui.link_target("EXCHANGE")
                ui.label('学园交流会').style('font-size: x-large')
                
            list_edit_area(config.configdict["EXCHANGE_HIGHEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]])

            with ui.row():
                ui.link_target("ACTIVITY")
                ui.label('活动关卡').style('font-size: x-large')

            list_edit_area(config.configdict["EVENT_QUEST_LEVEL"], ["天刷取", "", ["关卡", "次数"]])
                

            with ui.row():
                ui.link_target("HARD")
                ui.label('困难关卡').style('font-size: x-large')
                
            list_edit_area(config.configdict["HARD"], ["天刷取", "", ["地区", "关卡", "次数"]])
                
            with ui.row():
                ui.link_target("NORMAL")
                ui.label('普通关卡').style('font-size: x-large')
            
            list_edit_area(config.configdict["NORMAL"], ["天刷取", "", ["地区", "关卡", "次数"]])
                
            with ui.row():
                ui.link_target("TOOL_PATH")
                ui.label('其他设置').style('font-size: x-large')
            
            with ui.row():
                ui.number('点击后停顿时间', 
                          suffix="s",
                          step=0.1,
                          precision=1).bind_value(config.configdict, 'TIME_AFTER_CLICK')
            
            with ui.row():
                ui.input('ADB路径').bind_value(config.configdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.input('截图名称').bind_value(config.configdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
                
            with ui.column().style('width: 10vw; overflow: auto; position: fixed; bottom: 20px; right: 20px;min-width: 150px;'):
                def save_and_alert():
                    config.save_config(load_jsonname)
                    ui.notify("保存成功")
                ui.button('保存配置', on_click=save_and_alert)