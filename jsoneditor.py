if __name__ in {"__main__", "__mp_main__"}:
    try:
        import os
        # 获取到当前文件夹下以json为后缀的文件
        def get_json_list():
            return [i for i in os.listdir() if i.endswith(".json")]

        # 如果没有config.json文件，则创建一个
        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                f.write("{}")
        # 维护当前正在看的json文件名字
        now_json_name = {"name":"config.json"}

        from gui import show_GUI
        from nicegui import native, ui
        
        @ui.refreshable
        def draw_upper_right_selectlist(jsonfile_list):
            """
            更新右上角的选择列表，并自动保存当前config文件
            当选择列表发生变化时，会自动调用show_GUI.refresh()函数
            """
            with ui.column().style('width: 10vw; overflow: auto; position: fixed; top: 20px; right: 20px;min-width: 150px;'):
                # now_json_name主要是初始值有用
                # 不在select里设置value，只有后面的bind_value的话，渲染时会触发一次on_change事件
                ui.select(jsonfile_list, value=now_json_name["name"], on_change=lambda:show_GUI.refresh(now_json_name['name'])).bind_value(now_json_name, 'name')
        
        show_GUI("config.json")
        draw_upper_right_selectlist(get_json_list())
        
        
        ui.timer(10.0, lambda: draw_upper_right_selectlist.refresh(get_json_list()))
        ui.run(native=True, window_size=(1280, 720), title="Blue Archive Aris Helper", favicon="./assets/favicon.ico", language="zh-cn", reload=False, port=native.find_open_port())
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("按任意键退出")