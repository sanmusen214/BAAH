if __name__ in {"__main__", "__mp_main__"}:
    import os
    # 获取到当前文件夹下以json为后缀的文件
    def get_json_list():
        return [i for i in os.listdir() if i.endswith(".json")]
    
    json_list = get_json_list()

    if len(json_list) == 0:
        # 如果没有json文件，则创建一个
        with open("config.json", "w") as f:
            f.write("{}")
    now_json_name = ["config.json"]

    from gui import show_GUI
    from nicegui import ui
    
    @ui.refreshable
    def draw_upper_right_selectlist(json_list, now_value_list):
        """
        更新右上角的选择列表，并自动保存当前config文件
        当选择列表发生变化时，会自动调用show_GUI.refresh()函数
        """
        with ui.column().style('width: 10vw; overflow: auto; position: fixed; top: 20px; right: 20px;min-width: 150px;'):
            ui.select(json_list, value=now_value_list[0], on_change=lambda y=now_value_list[0]:show_GUI.refresh(y))
    
    show_GUI("config.json")
    draw_upper_right_selectlist(get_json_list(), now_json_name)
    
    
    ui.timer(10.0, lambda: draw_upper_right_selectlist.refresh(get_json_list(), now_json_name))
    ui.run(native=True, window_size=(1280, 720), title="Blue Archive Aris Helper", favicon="./assets/favicon.ico", language="zh-cn")