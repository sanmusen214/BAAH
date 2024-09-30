import argparse
from nicegui import native, app, ui

g_token: str = ""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="host address", default="127.0.0.1")
    parser.add_argument("--port", help="host port", default=native.find_open_port())
    parser.add_argument("--token", help="password", default=None)
    args = parser.parse_args()
    global g_token
    g_token = args.token
    return args


def get_token() -> str:
    return g_token


def check_token_dialog(refresh_page):
    if len(g_token) != 0 and g_token != app.storage.user.get("token"):
        with ui.card().classes('absolute-center'):
            ui.input('Token', password=True, password_toggle_button=True,
                     on_change=lambda e: [app.storage.user.update({"token": e.value}),
                                          refresh_page.refresh() if e.value == g_token else None])
        return False
    else:
        return True
