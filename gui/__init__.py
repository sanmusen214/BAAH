from nicegui import ui
import os
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
        "SHOP_NORMAL",
        "SHOP_CONTEST",
        "TASK_ACTIVATE"
    ]
    
    all_str_key_names = [
        "TARGET_EMULATOR_PATH",
        "PIC_PATH",
        "ACTIVITY_PATH",
        "ADB_PATH",
        "SCREENSHOT_NAME",
        "TARGET_IP_PATH",
    ]
    
    all_num_key_names = [
        "TARGET_PORT",
        "TIME_AFTER_CLICK",
        "RESPOND_Y",
    ]
    
    server_map = {
        "server2pic": {
            "日服":"./assets_jp",
            "国际服":"./assets",
            "国服官服":"./assets_cn",
            "国服B服":"./assets_cn"
        },
        "server2activity": {
            "日服":"com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
            "国际服":"com.nexon.bluearchive/.MxUnityPlayerActivity",
            "国服官服":"com.RoamingStar.BlueArchive/com.yostar.sdk.bridge.YoStarUnityPlayerActivity",
            "国服B服":"com.RoamingStar.BlueArchive.bilibili/com.yostar.sdk.bridge.YoStarUnityPlayerActivity"
        },
        "activity2server": {
            "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity":"日服",
            "com.nexon.bluearchive/.MxUnityPlayerActivity":"国际服",
            "com.RoamingStar.BlueArchive/com.yostar.sdk.bridge.YoStarUnityPlayerActivity":"国服官服",
            "com.RoamingStar.BlueArchive.bilibili/com.yostar.sdk.bridge.YoStarUnityPlayerActivity":"国服B服"
        },
        "server2respond": {
            "日服":40,
            "国际服":40,
            "国服官服":60,
            "国服B服":40
        }
    }
    
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
            elif key == "PIC_PATH":
                server = server_map["activity2server"][config.configdict['ACTIVITY_PATH']]
                config.configdict[key] = server_map["server2pic"][server]
            elif key == "TARGET_IP_PATH":
                config.configdict[key] = "127.0.0.1"
            else:
                config.configdict[key] = ""
    for key in all_num_key_names:
        if key not in config.configdict:
            if key == "TARGET_PORT":
                config.configdict[key] = 5555
            elif key == "RESPOND_Y":
                config.configdict[key] = 40
            elif key == "TIME_AFTER_CLICK":
                config.configdict[key] = 0.7
            else:
                config.configdict[key] = 1
    # 判断TASK_ACTIVATE长度与TASK_ORDER长度是否一致
    if len(config.configdict["TASK_ACTIVATE"]) != len(config.configdict["TASK_ORDER"]):
        # 给TASK_ACTIVATE添加len(TASK_ORDER)的True
        for i in range(len(config.configdict["TASK_ORDER"])):
            config.configdict["TASK_ACTIVATE"].append(True)
        # 截取TASK_ACTIVATE前len(TASK_ORDER)个
        config.configdict["TASK_ACTIVATE"] = config.configdict["TASK_ACTIVATE"][:len(config.configdict["TASK_ORDER"])]
    
    
    
    all_task_names = list(task_dict.keys())
    
    
    
    # =============================================
    
    def list_edit_area(datadict, linedesc, blockdesc=""):
        """
        datadict: 要修改的二维或三维列表，长度代表列表维度
            [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
        linedesc: 二维或三维列表的描述，长度代表列表维度
        blockdesc: 对于这个块的描述
        """
        dim = len(linedesc)
        subdim = 0
        if dim == 3:
            subdim = len(linedesc[2])
        @ui.refreshable
        def item_list():
            for blocklinedesc in blockdesc.split('\n'):
                ui.label(f'{blocklinedesc}')
            for i in range(len(datadict)):
                line_item = datadict[i]
                ui.label(f'第{i+1}{linedesc[0]}: ')
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
                ui.link('课程表/日程', '#COURSE_TABLE')
                ui.link('商店', '#SHOP_NORMAL')
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
            
            server = ui.radio(["日服", "国际服", "国服官服","国服B服"], value=server_map["activity2server"][config.configdict['ACTIVITY_PATH']], on_change=lambda a:set_server_info(a.value)).props('inline')
            
            def set_server_info(server):
                config.configdict["PIC_PATH"] = server_map["server2pic"][server]
                config.configdict["ACTIVITY_PATH"] = server_map["server2activity"][server]
                config.configdict["RESPOND_Y"] = server_map["server2respond"][server]
                
            
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
                        acheck = ui.checkbox('启用', value=config.configdict["TASK_ACTIVATE"][i], on_change=lambda v,i=i: config.configdict["TASK_ACTIVATE"].__setitem__(i, v.value))
                        if i==0:
                            atask.set_enabled(False)
                            acheck.set_enabled(False)
                        ui.button("添加任务", on_click=lambda i=i+1: add_task(i))
                        if len(config.configdict["TASK_ORDER"]) > 0 and i > 0:
                            ui.button("删除任务", on_click=lambda i=i: del_task(i), color="red")

            def add_task(i):
                config.configdict["TASK_ORDER"].insert(i, "邮件")
                config.configdict["TASK_ACTIVATE"].insert(i, True)
                task_order.refresh()
            
            def del_task(i):
                config.configdict["TASK_ORDER"].pop(i)
                config.configdict["TASK_ACTIVATE"].pop(i)
                task_order.refresh()
            
            task_order()
            
            with ui.row():
                ui.link_target("NEXT_CONFIG")
                ui.label('后续配置文件').style('font-size: x-large')
            
            ui.label("注意：此项配置文件会在当前配置文件执行完毕后继续执行，比如config.json是登录的国际服，那么你可以讲config.json复制一份重命名为config2.json。在config2.json里将区服改为日服").style('color: red')
            ui.label("如果你只想运行config.json一个配置文件的话此项直接不填").style('color: red')
            
                
            ui.input('执行完此配置文件过后，继续执行配置文件').bind_value(config.configdict, 'NEXT_CONFIG',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.link_target("COURSE_TABLE")
                ui.label('课程表/日程').style('font-size: x-large')
            
            list_edit_area(config.configdict["TIMETABLE_TASK"], ["个地区", "房间"], "其中地区指课程表/日程右侧那些列表的不同选项卡（夏莱办公室，夏莱居住区等）\n房间指课程表/日程每个学院里的房间，从左往右从上往下数，数字从1到9\n如果某个地区没有设置点击的房间则会跳过那个地区")
                
            with ui.row():
                ui.link_target("SHOP_NORMAL")
                ui.label('商店（一般）').style('font-size: x-large')
            
            list_edit_area(config.configdict["SHOP_NORMAL"], ["行", "物品"], "其中行数指普通商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")
            
            with ui.row():
                ui.link_target("SHOPCONTEST")
                ui.label('商店（战术大赛）').style('font-size: x-large')
                
            list_edit_area(config.configdict["SHOP_CONTEST"], ["行", "物品"], "其中行数指竞技场商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")
            
            with ui.row():
                ui.link_target("WANTED")
                ui.label('悬赏通缉').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["WANTED_HIGHEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。\n悬赏通缉的地区就是指进入悬赏通缉页面之后右侧那三个不同的地区（高架公路，沙漠铁道，教室）")
            
            
            with ui.row():
                ui.link_target("SPECIAL_TASK")
                ui.label('特殊任务').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["SPECIAL_HIGHTEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]],"一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。\n特殊任务的地区就是指进入特殊任务页面之后右侧第几个不同的刷取关（经验，金币）")
            
            with ui.row():
                ui.link_target("EXCHANGE")
                ui.label('学园交流会').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["EXCHANGE_HIGHEST_LEVEL"], ["天刷取", "", ["学院", "关卡", "次数"]],"一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。\n学学院就是指进入学园交流会页面之后右侧第几个学院（三一，格黑娜，千年）")

            with ui.row():
                ui.link_target("ACTIVITY")
                ui.label('活动关卡').style('font-size: x-large')

            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["EVENT_QUEST_LEVEL"], ["天刷取", "", ["关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。")
                

            with ui.row():
                ui.link_target("HARD")
                ui.label('困难关卡').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["HARD"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。")
                
            with ui.row():
                ui.link_target("NORMAL")
                ui.label('普通关卡').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。国服暂未实装扫荡max次')
            list_edit_area(config.configdict["NORMAL"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。")
                
            with ui.row():
                ui.link_target("TOOL_PATH")
                ui.label('其他设置').style('font-size: x-large')
                
            ui.label("注意：以下设置不建议修改，除非你知道你在干什么").style('color: red')
            
            with ui.row():
                ui.number('点击后停顿时间', 
                          suffix="s",
                          step=0.1,
                          precision=1).bind_value(config.configdict, 'TIME_AFTER_CLICK')
                
            with ui.row():
                ui.number("滑动触发距离",
                          step=1,
                          min=1,
                          precision=0).bind_value(config.configdict, 'RESPOND_Y').set_enabled(False)
                
            with ui.row():
                ui.input("模拟器监听IP地址（此项不包含端口号）").bind_value(config.configdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.input('ADB.exe路径').bind_value(config.configdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.input('截图名称').bind_value(config.configdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
                
            with ui.column().style('width: 10vw; overflow: auto; position: fixed; bottom: 40px; right: 20px;min-width: 150px;'):
                def save_and_alert():
                    config.save_config(load_jsonname)
                    ui.notify("保存成功")
                ui.button('保存配置', on_click=save_and_alert)

                def save_and_alert_and_run():
                    config.save_config(load_jsonname)
                    ui.notify("保存成功")
                    ui.notify("开始执行")
                    # 打开同目录中的BAAH.exe
                    os.system(f"start BAAH{MyConfigger.NOWVERSION}.exe")
                ui.button('保存配置并执行', on_click=save_and_alert_and_run)
            
            # 加载完毕保存一下config，让新建的config文件有默认值
            config.save_config(load_jsonname)