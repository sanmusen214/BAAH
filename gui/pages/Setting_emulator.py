from nicegui import ui, run
from modules.utils.adb_utils import connect_to_device, mumu_rm_mu, mumu_bak_mu, NO_NEED, ERROR, FAILED, SUCCESS, NO_FILE


def set_emulator(config):
    
    def noti_user(res):
        ui.notify(res)
        if res == NO_NEED:
            ui.notify("无需操作")
        elif res == ERROR:
            ui.notify("操作失败。请检查所需条件，查看命令窗口报错")
        elif res == FAILED:
            ui.notify("操作失败")
        elif res == SUCCESS:
            ui.notify("操作成功")
        elif res == NO_FILE:
            ui.notify("未找到备份的DATA/mu_bak文件")
        else:
            ui.notify("未知响应")
    
    async def fix_mumu_jp_server(cfig):
        """修复MUMU模拟器日服无法登录问题"""
        ui.notify("运行中...")
        connect_to_device(cfig)
        res = await run.io_bound(mumu_rm_mu, cfig)
        noti_user(res)

    async def back_mumu_root(cfig):
        """通过粘贴mu_bak文件恢复MUMU模拟器ROOT状态"""
        ui.notify("运行中...")
        connect_to_device(cfig)
        res = await run.io_bound(mumu_bak_mu, cfig)
        noti_user(res)
    
    
    ui.link_target("EMULATOR")
    ui.label(config.get_text("setting_emulator")).style('font-size: x-large')
    
    
    with ui.row().bind_visibility_from(config.userconfigdict, "TARGET_PORT", lambda v: v>=16384):
        with ui.card():
            ui.label("修复MUMU模拟器日服无法登录问题/FIX MUMU JP Server Login Issue").style('font-size: large')
            ui.label("修复前请手动设置以下内容，修复中遇到弹窗请点击 允许/Settings：")
            ui.label("1. 设置-其他-开启手机ROOT权限/Enable the ROOT permission")
            ui.label("2. 设置-磁盘-磁盘共享-可写系统盘 (重启)/Enable the writable system disk (restart)")
            with ui.row():
                ui.button("修复无法登录问题(删除ROOT/Delete ROOT)", on_click=lambda c=config:fix_mumu_jp_server(c))
                ui.button("重新ROOT(Re ROOT)", on_click=lambda c=config:back_mumu_root(c), color="normal")
            ui.label("修复完请直接重开模拟器")

    with ui.row():
        # IP+端口
        ui.number(config.get_text("config_emulator_port"),
                step=1,
                precision=0,
                ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v), backward=lambda v:int(v)).style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: not v)
        # 序列号
        ui.input(config.get_text("adb_serial")).bind_value(config.userconfigdict, 'ADB_SEIAL_NUMBER').style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: v)
        
        # 切换使用序列号还是IP+端口
        ui.checkbox(config.get_text("adb_direct_use_serial")).bind_value(config.userconfigdict, 'ADB_DIRECT_USE_SERIAL_NUMBER')
        
    
    with ui.row():
        kill_port = ui.checkbox(config.get_text("config_kill_port")).bind_value(config.userconfigdict, "KILL_PORT_IF_EXIST")
        kill_port.set_value(False)
        kill_port.set_enabled(False)
    
    with ui.row():    
        ui.input(config.get_text("config_emulator_path"),
                    ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')
    
    ui.checkbox(config.get_text("config_close_emulator_and_baah")).bind_value(config.userconfigdict, 'CLOSE_EMULATOR_BAAH')