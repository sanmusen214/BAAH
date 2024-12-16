def main():
    # Use freeze_support to avoid running GUI again: https://blog.csdn.net/fly_leopard/article/details/121610641
    import multiprocessing
    multiprocessing.freeze_support()
    if not multiprocessing.get_start_method(allow_none=True):
        from gui.components.check_update import check_version
        from gui.components.exec_arg_parse import parse_args
        from modules.configs.MyConfig import MyConfigger
        from nicegui import ui, app
        
        print("GUI is running...")
        args = parse_args()
        app.on_connect(check_version)
        ui.run(title=f"BAAH{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-cn",
            reload=False, host=args.host, port=args.port, show=args.show, storage_secret="32737")

if __name__ in {"__main__", "__mp_main__"}:
    main()
