if __name__ in {"__main__", "__mp_main__"}:
    try:
        import os
        import requests
        import sys
        from modules.configs.MyConfig import MyConfigger, config
        # 是否以网页形式运行
        isweb=False
        if len(sys.argv) > 1:
            isweb = sys.argv[1] == "web"
        # 获取到user config文件夹下以json为后缀的文件
        def get_json_list():
            return [i for i in os.listdir(MyConfigger.USER_CONFIG_FOLDER) if i.endswith(".json")]

        # 如果没有config.json文件，则创建一个
        if not os.path.exists(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json")):
            with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, "config.json"), "w") as f:
                f.write("{}")

        from gui import show_GUI
        from nicegui import native, ui, run

        alljson_list = get_json_list()
        alljson_tab_list = [None for i in alljson_list]
        
        with ui.tabs().classes('w-full') as tabs:
            for i,jsonname in enumerate(alljson_list):
                alljson_tab_list[i] = ui.tab(jsonname)
        with ui.tab_panels(tabs, value="config.json").classes('w-full'):
            for i,tab_panel in enumerate(alljson_tab_list):
                with ui.tab_panel(tab_panel).style("height: 88vh; overflow: auto;"):
                    show_GUI(alljson_list[i], MyConfigger())
        
        # 运行GUI
        if not isweb:
            try:
                ui.run(native=True, window_size=(1280,720), title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./assets/aris.ico", language="zh-cn", reload=False, port=native.find_open_port())
            except:
                # 如果GUI出错，自动使用网页端
                print("窗口端GUI出错，自动使用网页端/Window GUI error, automatically use web GUI")
                ui.run(title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./assets/aris.ico", language="zh-cn", reload=False, port=native.find_open_port())
        else:
            ui.run(title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./assets/aris.ico", language="zh-cn", reload=False, port=native.find_open_port())

    except Exception as e:
        import traceback
        traceback.print_exc()
        input("按任意键退出")