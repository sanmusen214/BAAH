from nicegui import ui
import os
import json
from modules.configs.MyConfig import MyConfigger
from modules.AllTask.myAllTask import task_dict
import hashlib

@ui.refreshable
def show_GUI(load_jsonname):
    
    with ui.row():
        ui.label("Blue Archive Aris Helper").style('font-size: xx-large')
    
    ui.label("BAAH可以帮助你完成碧蓝档案/蔚蓝档案的日服，国际服，国服官服，国服B服的每日任务")
    ui.label("QQ群：441069156")

    ui.label("获取最新版本可以到Github下载，或进群下载")
    
    ui.label("模拟器分辨率请设置为1280*720，240DPI!").style('color: red; font-size: x-large')
    
    config = MyConfigger(load_jsonname)
    # 在GUI里，我们只使用config.userconfigdict这个字典，不用config下的属性

    # myAllTask里面的key与GUI显示的key的映射
    real_taskname_to_show_taskname = {
        "登录游戏":"登录游戏",
        "清momotalk":"清momotalk",
        "咖啡馆":"咖啡馆",
        "咖啡馆只摸头":"咖啡馆只摸头",
        "课程表":"课程表/日程",
        "社团":"社团",
        "商店":"商店",
        "悬赏通缉":"悬赏通缉/指名手配",
        "特殊任务":"特殊任务/委托/依赖",
        "学园交流会":"学园交流会",
        "战术大赛":"战术大赛/竞技场",
        "困难关卡":"困难关卡",
        "活动关卡":"活动关卡",
        "每日任务":"每日任务",
        "邮件":"邮件",
        "普通关卡":"普通关卡",
    }

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
                                        ).style('width: 60px')
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
                                                    ).style('width: 60px')
                                
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

    with ui.row().style('min-width: 800px; display: flex; flex-direction: row;flex-wrap: nowrap;'):
        with ui.column().style('width: 200px; overflow: auto;flex-grow: 1;position: sticky; top: 20px;'):
            with ui.card():
                ui.link('模拟器配置', '#EMULATOR')
                ui.link('服务器配置', '#SERVER')
                ui.link('任务执行顺序', '#TASK_ORDER')
                ui.link('后续配置文件', '#NEXT_CONFIG')
                ui.link('咖啡馆', '#CAFE')
                ui.link('课程表/日程', '#COURSE_TABLE')
                ui.link('商店', '#SHOP_NORMAL')
                ui.link('悬赏通缉/指名手配', '#WANTED')
                ui.link('特殊任务/委托/依赖', '#SPECIAL_TASK')
                ui.link('学园交流会', '#EXCHANGE')
                ui.link('活动关卡', '#ACTIVITY')
                ui.link('困难关卡', '#HARD')
                ui.link('普通关卡', '#NORMAL')
                ui.link('其他设置', '#TOOL_PATH')


        with ui.column().style('flex-grow: 4;'):
            with ui.row():
                ui.link_target("EMULATOR")
                ui.label('模拟器配置').style('font-size: x-large')
                
            with ui.row():
                ui.number('模拟器端口',
                        step=1,
                        precision=0,
                        ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v)).style('width: 400px')
            with ui.row():    
                ui.input('模拟器路径'
                         ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')

            with ui.row():
                ui.link_target("SERVER")
                ui.label('服务器配置').style('font-size: x-large')
            
            server = ui.radio(["日服", "国际服", "国服官服","国服B服"], value=server_map["activity2server"][config.userconfigdict['ACTIVITY_PATH']], on_change=lambda a:set_server_info(a.value)).props('inline')
            
            def set_server_info(server):
                config.userconfigdict["PIC_PATH"] = server_map["server2pic"][server]
                config.userconfigdict["ACTIVITY_PATH"] = server_map["server2activity"][server]
                if config.userconfigdict["LOCK_SERVER_TO_RESPOND_Y"]:
                    config.userconfigdict["RESPOND_Y"] = server_map["server2respond"][server]
                
            
            # with ui.row():
            #     ui.input('匹配模板图片路径').bind_value(config.userconfigdict, 'PIC_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
                
            # with ui.row():
            #     ui.input('游戏包名').bind_value(config.userconfigdict, 'ACTIVITY_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.link_target("TASK_ORDER")
                ui.label('任务执行顺序').style('font-size: x-large')
            
            
            def select_clear_all_and_refresh_task_order(type="select"):
                if type == "select":
                    for i in range(1, len(config.userconfigdict["TASK_ACTIVATE"])):
                        config.userconfigdict["TASK_ACTIVATE"][i] = True
                else:
                    for i in range(1, len(config.userconfigdict["TASK_ACTIVATE"])):
                        config.userconfigdict["TASK_ACTIVATE"][i] = False
                task_order.refresh()
            
            with ui.row():
                ui.button("全选", on_click=lambda: select_clear_all_and_refresh_task_order("select"))
                ui.button("全不选", on_click=lambda: select_clear_all_and_refresh_task_order("unselect"))
            
            @ui.refreshable
            def task_order():
                for i in range(len(config.userconfigdict["TASK_ORDER"])):
                    with ui.row():
                        ui.label(f'第{i+1}个任务:')
                        atask = ui.select(real_taskname_to_show_taskname,
                                  value=config.userconfigdict["TASK_ORDER"][i],
                                  on_change=lambda v,i=i: config.userconfigdict["TASK_ORDER"].__setitem__(i, v.value),
                                  )
                        acheck = ui.checkbox('启用', value=config.userconfigdict["TASK_ACTIVATE"][i], on_change=lambda v,i=i: config.userconfigdict["TASK_ACTIVATE"].__setitem__(i, v.value))
                        if i==0:
                            atask.set_enabled(False)
                            acheck.set_enabled(False)
                        ui.button("添加任务", on_click=lambda i=i+1: add_task(i))
                        if len(config.userconfigdict["TASK_ORDER"]) > 0 and i > 0:
                            ui.button("删除任务", on_click=lambda i=i: del_task(i), color="red")

            def add_task(i):
                config.userconfigdict["TASK_ORDER"].insert(i, "邮件")
                config.userconfigdict["TASK_ACTIVATE"].insert(i, True)
                task_order.refresh()
            
            def del_task(i):
                config.userconfigdict["TASK_ORDER"].pop(i)
                config.userconfigdict["TASK_ACTIVATE"].pop(i)
                task_order.refresh()
            
            task_order()
            
            with ui.row():
                ui.link_target("NEXT_CONFIG")
                ui.label('后续配置文件').style('font-size: x-large')
            
            ui.label("注意：此项配置文件会在当前配置文件执行完毕后继续执行，比如config_global.json是登录的国际服，那么你可以把config_global.json复制一份重命名为config_jp.json。在config_jp.json里将区服改为日服").style('color: red')
            ui.label("如果你只想运行此配置文件的话此项直接不填").style('color: red')
            
                
            ui.input('执行完此配置文件过后，继续执行配置文件').bind_value(config.userconfigdict, 'NEXT_CONFIG',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.link_target("CAFE")
                ui.label('咖啡馆').style('font-size: x-large')
            
            ui.label("国服目前咖啡馆的视角无法继承，请取消勾选以下这项").style('color: red')
            ui.label("国际服/日服咖啡馆请将视角拉到最高，保持勾选以下这项")
            
            with ui.row():
                ui.checkbox("进入咖啡馆时视角是最高").bind_value(config.userconfigdict, "CAFE_CAMERA_FULL")
            
            with ui.row():
                ui.link_target("COURSE_TABLE")
                ui.label('课程表/日程').style('font-size: x-large')
            
            list_edit_area(config.userconfigdict["TIMETABLE_TASK"], ["个地区", "房间"], "其中地区指课程表/日程右侧那些列表的不同选项卡（夏莱办公室，夏莱居住区等）\n房间指课程表/日程每个学院里的房间，从左往右从上往下数，数字从1到9\n如果某个地区没有设置点击的房间则会跳过那个地区")
                
            with ui.row():
                ui.link_target("SHOP_NORMAL")
                ui.label('商店（一般）').style('font-size: x-large')
            
            
            ui.number(
                    '商店（一般）刷新次数',
                    step=1,
                    precision=0,
                    min=0,
                    max=3
                    ).bind_value(config.userconfigdict, 'SHOP_NORMAL_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
            
            list_edit_area(config.userconfigdict["SHOP_NORMAL"], ["行", "物品"], "其中行数指普通商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")
            
            with ui.row():
                ui.link_target("SHOPCONTEST")
                ui.label('商店（战术大赛）').style('font-size: x-large')
                
            ui.number(
                    '商店（战术大赛）刷新次数',
                    step=1,
                    precision=0,
                    min=0,
                    max=3
                    ).bind_value(config.userconfigdict, 'SHOP_CONTEST_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
                
            list_edit_area(config.userconfigdict["SHOP_CONTEST"], ["行", "物品"], "其中行数指竞技场商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")
            
            with ui.row():
                ui.link_target("WANTED")
                ui.label('悬赏通缉').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["WANTED_HIGHEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。\n悬赏通缉的地区就是指进入悬赏通缉页面之后右侧那三个不同的地区（高架公路，沙漠铁道，教室）")
            
            
            with ui.row():
                ui.link_target("SPECIAL_TASK")
                ui.label('特殊任务/特别委托').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["SPECIAL_HIGHTEST_LEVEL"], ["天刷取", "", ["地区", "关卡", "次数"]],"一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。\n特殊任务的地区就是指进入页面之后右侧第几个不同的刷取关（经验，金币）")
            
            with ui.row():
                ui.link_target("EXCHANGE")
                ui.label('学园交流会').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["EXCHANGE_HIGHEST_LEVEL"], ["天刷取", "", ["学院", "关卡", "次数"]],"一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。\n学学院就是指进入学园交流会页面之后右侧第几个学院（三一，格黑娜，千年）")

            with ui.row():
                ui.link_target("ACTIVITY")
                ui.label('活动关卡').style('font-size: x-large')

            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["EVENT_QUEST_LEVEL"], ["天刷取", "", ["关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。")
                

            with ui.row():
                ui.link_target("HARD")
                ui.label('困难关卡').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["HARD"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。")
                
            with ui.row():
                ui.link_target("NORMAL")
                ui.label('普通关卡').style('font-size: x-large')
            
            ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
            list_edit_area(config.userconfigdict["NORMAL"], ["天刷取", "", ["地区", "关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。")
                
            with ui.row():
                ui.link_target("TOOL_PATH")
                ui.label('其他设置').style('font-size: x-large')
                
            ui.label("注意：以下设置不建议修改，除非你知道你在干什么").style('color: red')
            
            with ui.row():
                ui.number('点击后停顿时间', 
                          suffix="s",
                          step=0.1,
                          precision=1).bind_value(config.userconfigdict, 'TIME_AFTER_CLICK')
            
            ui.label("滑动过头此项调小60->40，滑动距离不够此项调大40->60")
            with ui.row():
                ui.number("滑动触发距离",
                          step=1,
                          min=1,
                          precision=0).bind_value(config.userconfigdict, 'RESPOND_Y', forward=lambda x:int(x), backward=lambda x:int(x)).bind_enabled(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y', forward=lambda v: not v, backward=lambda v: not v)
                ui.checkbox("与区服绑定(国服官服60，其他40)").bind_value(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y')
                
            with ui.row():
                ui.input("模拟器监听IP地址（此项不包含端口号）").bind_value(config.userconfigdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.input('ADB.exe路径').bind_value(config.userconfigdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
            
            with ui.row():
                ui.input('截图名称').bind_value(config.userconfigdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px').set_enabled(False)
                
            with ui.column().style('width: 10vw; overflow: auto; position: fixed; bottom: 40px; right: 20px;min-width: 150px;'):
                def save_and_alert():
                    config.save_config(load_jsonname)
                    ui.notify("保存成功")
                ui.button('保存配置', on_click=save_and_alert)

                def save_and_alert_and_run():
                    config.save_config(load_jsonname)
                    ui.notify("保存成功")
                    ui.notify("开始执行")
                    # 打开同目录中的BAAH.exe，传入当前config的json文件名
                    os.system(f"start BAAH{MyConfigger.NOWVERSION}.exe {load_jsonname}")
                ui.button('保存并执行此配置', on_click=save_and_alert_and_run)
            
            # 加载完毕保存一下config，让新建的config文件有默认值
            config.save_config(load_jsonname)