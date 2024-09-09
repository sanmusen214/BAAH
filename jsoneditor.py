if __name__ in {"__main__", "__mp_main__"}:
    try:
        import os
        import requests
        import sys
        from modules.configs.MyConfig import MyConfigger, config
        print("参数：", sys.argv)
        # 获取到user config文件夹下以json为后缀的文件
        def get_json_list():
            return [i for i in os.listdir(MyConfigger.USER_CONFIG_FOLDER) if i.endswith(".json")]

        from gui import show_gui
        from gui.components.check_update import only_check_version
        from nicegui import native, ui, run, app
        
        import argparse

        # 解析器
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", help="host address", default="127.0.0.1")
        parser.add_argument("--port", help="host port", default=native.find_open_port())
        parser.add_argument("--token", help="password", default=None)
        args = parser.parse_args()


        alljson_list = get_json_list()
        alljson_tab_list = [None for i in alljson_list]

        # 如果没有config.json文件且alljson_list长度为0，则创建一个
        if len(alljson_list)==0 and not os.path.exists(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json")):
            with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json"), "w") as f:
                f.write("{}")
            # 重新构造alljson_list和alljson_tab_list
            alljson_list = get_json_list()
            alljson_tab_list = [None for i in alljson_list]


        async def add_new_config():
            """
            点击加号后，添加一个新的json配置文件到alljson_list和alljson_tab_list里，然后让Configger类去新建这个json文件
            """
            response = await ui.run_javascript('''
                return await window.prompt("请输入新配置名/Please input new config name")
            ''', timeout = 60.0)
            if not response:
                print("未输入配置名/No config name input")
                return
            print("输入的配置名/Input config name:", response)
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
                        show_gui(alljson_list[i])
        check_times = 0
        async def check_version():
            """check the version, show the update message"""
            global check_times
            # if users have opened multi pages, this function will be called multi times
            if check_times > 0:
                return
            check_times = 1
            result = await only_check_version()
            if not result["status"]:
                return
            ui.notify(result["msg"], close_button=True, type="info")
            with updateTextBox:
                ui.link(result["msg"], "https://github.com/sanmusen214/BAAH/releases", new_tab=True).style("color: red; border: 1px solid blue; border-radius: 5px; font-size: 20px;z-index: 9999;")
        
        # 更新提示
        app.on_connect(check_version)
        updateTextBox = ui.row().style("position: fixed;z-index: 9999;")

        @ui.refreshable
        def showContentArea() -> None:
            """
            主要内容区域
            """
            if args.token and args.token != app.storage.user.get("token"):
                # token输入页面
                with ui.card().classes('absolute-center'):
                    ui.input('Token', password=True, password_toggle_button=True,
                    on_change=lambda e: [app.storage.user.update({"token": e.value}), showContentArea.refresh() if e.value == args.token else None])
            else:
                # Tab栏区域
                tab_area()

        # 放进页面，提供app.storage.user存储能力
        @ui.page('/')
        def MainPage() -> None:
            showContentArea()

        # 运行GUI
        ui.run(title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn", reload=False, host=args.host, port=args.port)

    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter to quit...")