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
        from gui.components.check_update import only_check_version
        from nicegui import native, ui, run, app

        from typing import Optional

        from fastapi import Request
        from fastapi.responses import RedirectResponse
        from starlette.middleware.base import BaseHTTPMiddleware

        import argparse

        unrestricted_page_routes = {'/login'}
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", help="host address", default="127.0.0.1")
        parser.add_argument("--auth", help="enable authentication, only for web", action="store_true")
        parser.add_argument("--username", help="username", default="admin")
        parser.add_argument("--password", help="password", default="admin")
        args = parser.parse_args()

        passwords = {
            args.username: args.password,
        }
        

        class AuthMiddleware(BaseHTTPMiddleware):
            """This middleware restricts access to all NiceGUI pages.

            It redirects the user to the login page if they are not authenticated.
            """

            async def dispatch(self, request: Request, call_next):
                if not app.storage.user.get('authenticated', False):
                    if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                        app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                        return RedirectResponse('/login')
                return await call_next(request)


        if (open_state["OPEN_IN_WEB"] and args.auth):
            app.add_middleware(AuthMiddleware)

        alljson_list = get_json_list()
        alljson_tab_list = [None for i in alljson_list]

        @ui.page('/login')
        def login() -> Optional[RedirectResponse]:
            def try_login() -> None:  # local function to avoid passing username and password as arguments
                if passwords.get(username.value) == password.value:
                    app.storage.user.update({'username': username.value, 'authenticated': True})
                    ui.open('/')  # go back to where the user wanted to go
                else:
                    ui.notify('Wrong username or password', color='negative')

            if app.storage.user.get('authenticated', False):
                return RedirectResponse('/')
            with ui.card().classes('absolute-center'):
                username = ui.input('Username').on('keydown.enter', try_login)
                password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
                ui.button('Log in', on_click=try_login)
            return None


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
                        show_GUI(alljson_list[i], MyConfigger(), shared_softwareconfig)
        check_times = 0
        async def check_version():
            """check the version, show the update message"""
            global check_times
            # if users have opened multi pages, this function will be called multi times
            if check_times > 0:
                return
            check_times = 1
            result = await only_check_version(shared_softwareconfig)
            if not result["status"]:
                return
            ui.notify(result["msg"], close_button=True, type="info")
            with updateTextBox:
                ui.link(result["msg"], "https://github.com/sanmusen214/BAAH/releases", new_tab=True).style("color: red; border: 1px solid blue; border-radius: 5px; font-size: 20px;z-index: 9999;")
        
        # 更新提示
        app.on_connect(check_version)
        updateTextBox = ui.row().style("position: fixed;z-index: 9999;")
        # Tab栏区域
        tab_area()

        # 运行GUI
        print(open_state)
        if open_state["OPEN_IN_WEB"]:
            ui.run(title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn", reload=False, host=args.host, port=native.find_open_port(), storage_secret=MyConfigger.STORAGE_SECRET)
        else:
            ui.run(native=True, window_size=(1280,720), title=f"Blue Archive Aris Helper{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn", reload=False, host={args.host}, port=native.find_open_port())

    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter to quit...")