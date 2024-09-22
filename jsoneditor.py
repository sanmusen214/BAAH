from gui.components.check_update import check_version
from modules.configs.MyConfig import MyConfigger

from nicegui import ui, app


def main():
    app.on_connect(check_version)
    ui.run(title=f"BAAH{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-CN", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
