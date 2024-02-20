if __name__ in {"__main__", "__mp_main__"}:
    try:
        import os
        import requests
        import sys
        from modules.configs.MyConfig import MyConfigger, config
        # 是否以网页形式运行
        open_state = {
            "OPEN_IN_WEB": True
        }
        print("参数：", sys.argv)
        if len(sys.argv) > 1:
            if sys.argv[1] == "window":
                open_state["OPEN_IN_WEB"] = False
        # 获取到user config文件夹下以json为后缀的文件
        def get_json_list():
            return [i for i in os.listdir(MyConfigger.USER_CONFIG_FOLDER) if i.endswith(".json")]

        from gui import show_GUI
        from nicegui import native, ui, run

        alljson_list = get_json_list()
        alljson_tab_list = [None for i in alljson_list]
        
        # 如果没有config.json文件且alljson_list长度为0，则创建一个
        if len(alljson_list)==0 and not os.path.exists(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json")):
            with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json"), "w") as f:
                f.write("{}")
            # 重新构造alljson_list和alljson_tab_list
            alljson_list = get_json_list()
            alljson_tab_list = [None for i in alljson_list]
        
        # 构造一个config，用于在tab间共享softwareconfigdict
        shared_softwareconfig = MyConfigger()

        async def add_new_config():
            """
            点击加号后，添加一个新的json配置文件到alljson_list和alljson_tab_list里，然后让Configger类去新建这个json文件
            """
            response = await ui.run_javascript('''
                return await window.prompt("请输入新配置名/Please input new config name")
            ''', timeout = 15.0)
            if not response:
                return
            response = response.strip().replace(".json", "")
            response = response + ".json"
            if response in alljson_list:
                await ui.alert("配置名已存在/Config name already exists")
            else:
                # 创建一个新的json文件，延长alljson_list和alljson_tab_list
                alljson_list.append(response)
                alljson_tab_list.append(None)
                tab_area.refresh()

        @ui.refreshable
        def tab_area():
            with ui.tabs().classes('w-full') as tabs:
                for i,jsonname in enumerate(alljson_list):
                    alljson_tab_list[i] = ui.tab(jsonname, label=jsonname).style("text-transform: none;")
                # 新建配置，用加号添加
                ui.button("+", on_click=add_new_config).style("width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer;")
            with ui.tab_panels(tabs, value=alljson_list[0]).classes('w-full'):
                for i,tab_panel in enumerate(alljson_tab_list):
                    with ui.tab_panel(tab_panel).style("height: 88vh; overflow: auto;"):
                        show_GUI(alljson_list[i], MyConfigger(), shared_softwareconfig)

        # Tab栏区域
        tab_area()

        # 运行GUI
        print(open_state)
        if open_state["OPEN_IN_WEB"]:
            ui.run(title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn", reload=True, port=native.find_open_port())
        else:
            ui.run(native=True, window_size=(1280,720), title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn", reload=True, port=native.find_open_port())

    except Exception as e:
        import traceback
        traceback.print_exc()
        input("按任意键退出")