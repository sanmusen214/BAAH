from ..define import gui_shared_config

from nicegui import ui, run
import time
import requests
import os


async def only_check_version():
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
    resultdict = {}
    # 如果两个网站都访问失败
    if len(eachtime) == 0:
        ui.notify(gui_shared_config.get_text("notice_fail"))
        resultdict["status"] = False
        resultdict["msg"] = f'{gui_shared_config.get_text("notice_fail")} Fail to connect Github/Gitee'
        return resultdict
    # 找到访问时间最短的网站key
    fastestkey = min(eachtime, key=eachtime.get)
    # 判断是否需要更新
    if gui_shared_config.get_one_version_num(eachnewesttag[fastestkey]) > gui_shared_config.get_one_version_num():
        ui.notify(f'{gui_shared_config.get_text("notice_get_new_version")}: {eachnewesttag[fastestkey]} ({fastestkey})')
        resultdict["status"] = True
        resultdict["msg"] = f'{gui_shared_config.get_text("notice_get_new_version")}: {eachnewesttag[fastestkey]} ({fastestkey})'
        resultdict["urls"] = eachdowloadurl[fastestkey]
    else:
        ui.notify(gui_shared_config.get_text("notice_no_new_version"))
        resultdict["status"] = False
        resultdict["msg"] = gui_shared_config.get_text("notice_no_new_version")
    return resultdict

# 检查更新
async def get_newest_version(config):
    """检查最新版本并下载更新包"""
    ui.notify(config.get_text("button_check_version"))
    resultdict = await only_check_version(config)
    ui.notify(resultdict["msg"])
    if not resultdict["status"]:
        return
    # 下载
    ui.notify(config.get_text("notice_download_version"))
    target_urls = resultdict["urls"]
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