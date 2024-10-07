from gui.components.check_update import check_version
from gui.components.exec_arg_parse import parse_args
from modules.configs.MyConfig import MyConfigger

from nicegui import ui, app


def main():
    args = parse_args()
    app.on_connect(check_version)
    ui.run(title=f"BAAH{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn",
           reload=False, host=args.host, port=args.port, storage_secret="32737")

if __name__ in {"__main__", "__mp_main__"}:
    main()
