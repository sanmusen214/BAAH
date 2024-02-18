from nicegui import ui, run
import time
import requests
import os
import zipfile

def set_BAAH(config):
    
    def select_language(value):
        config.softwareconfigdict["LANGUAGE"] = value
        config.save_software_config()
        if value == "zh_CN":
            ui.notify("语言已切换为中文，重启生效")
        else:
            ui.notify("Language has been changed to English, restart to take effect")

    # 检查更新
    async def check_newest_version():
        ui.notify(config.get_text("button_check_version"))
        # 比较访问https://gitee.com/api/v5/repos/sammusen/BAAH/releases/latest和https://api.github.com/repos/sanmusen214/BAAH/releases/latest哪一个快
        urls={
            "gitee":"https://gitee.com/api/v5/repos/sammusen/BAAH/releases/latest",
            "github":"https://api.github.com/repos/sanmusen214/BAAH/releases/latest"
        }
        # 比较访问两个网站的时间，哪个快用哪个
        eachtime = {}
        # tag去掉BAAH字样
        eachnewesttag = {}
        eachdowloadurl = {}
        for key in urls:
            nowtime = time.time()
            try:
                r = await run.io_bound(requests.get, urls[key], timeout=5)
                if r.status_code == 200:
                    eachtime[key] = time.time() - nowtime
                    data = r.json()
                    eachnewesttag[key]=data["tag_name"].replace("BAAH", "")
                    eachdowloadurl[key]=[each["browser_download_url"] for each in data["assets"]]
            except:
                pass
        print(eachtime)
        print(eachnewesttag)
        print(eachdowloadurl)
        # 如果两个网站都访问失败
        if len(eachtime) == 0:
            ui.notify(config.get_text("notice_fail"))
            return
        # 找到访问时间最短的网站key
        fastestkey = min(eachtime, key=eachtime.get)
        # 判断是否需要更新
        if config.get_one_version_num(eachnewesttag[fastestkey]) > config.get_one_version_num():
            ui.notify(f'{config.get_text("notice_get_new_version")}: {eachnewesttag[fastestkey]} ({fastestkey})')
        else:
            ui.notify(config.get_text("notice_no_new_version"))
            return
        # 下载
        ui.notify(config.get_text("notice_download_version"))
        target_urls = eachdowloadurl[fastestkey]
        # 找到urls里面以_update.zip结尾的url
        target_url = ""
        for each in target_urls:
            if each.endswith("_update.zip"):
                target_url = each
                break
        # 下载target_url到当前目录
        if target_url == "":
            ui.notify(config.get_text("notice_fail"))
            return
        # 如果zip文件不在本地就下载
        targetfilename = target_url.split("/")[-1]
        if not os.path.exists(targetfilename):
            try:
                r = await run.io_bound(requests.get, target_url, timeout=10)
                
                if r.status_code == 200:
                    with open(targetfilename, "wb") as f:
                        f.write(r.content)
                    ui.notify(config.get_text("notice_download_version") + " : " +config.get_text("notice_success"))
                else:
                    ui.notify(config.get_text("notice_download_version") + " : " +config.get_text("notice_fail"))
                    return
            except:
                ui.notify(config.get_text("notice_download_version") + " : " +config.get_text("notice_fail"))
                return
        # 下载完成后解压
        # 将压缩包内BAAH文件夹内的文件解压到当前目录


        
    
    with ui.column():
        ui.link_target("BAAH")
        ui.label("Blue Archive Aris Helper").style('font-size: xx-large')
        
        ui.toggle({"zh_CN":"中文", "en_US":"English"}, value=config.softwareconfigdict["LANGUAGE"], on_change=lambda e:select_language(e.value))

        ui.label(config.get_text("BAAH_desc"))

        ui.label(config.get_text("BAAH_get_version"))

        ui.button(config.get_text("button_check_version"), on_click=check_newest_version)
        
        web_url = {
                    "github": "https://github.com/sanmusen214/BAAH",
                    "bilibili":"https://space.bilibili.com/7331920"
                }
        
        ui.input("Github").bind_value_from(web_url, "github").style('width: 400px')
        ui.input("Bilibili").bind_value_from(web_url, "bilibili").style('width: 400px')
        

        ui.label(config.get_text("BAAH_attention")).style('color: red; font-size: x-large')
        
        ui.html('<iframe  src="//player.bilibili.com/player.html?aid=539065954&bvid=BV1pi4y1W7QB&cid=1413492023&p=1&autoplay=0" width="720px" height="480px" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')