import hashlib
import json
import shutil
import subprocess
import traceback
import requests
import os
import zipfile
import time
import sys

updater_version = "0.3.2"
print(f"This Updator Version: {updater_version}")

def copy_to_temp_and_run():
    """
    如果当前文件不是temp，创造并运行temp

    返回True时，代表当前文件是update
    返回False时，代表当前文件是temp
    """
    # 获取当前文件的绝对路径
    # print(os.path.realpath(sys.argv[0]))
    path = os.path.realpath(sys.executable)
    # print(os.path.dirname(os.path.realpath(sys.argv[0])))
    print(f"This exe file path is: {path}")
    temp_update_name = "update_temp.exe"
    if not path.endswith(temp_update_name):
        # 复制此文件并且粘贴为temp.exe
        with open(path, "rb") as f:
            content = f.read()
        with open(temp_update_name, "wb") as f2:
            f2.write(content)
        # 执行temp.exe
        os.system(f'start {temp_update_name}')
        return True
    else:
        print(f"This is {temp_update_name}")
        return False

def get_one_version_num(versionstr):
    """
    将版本号字符串转换成数字
    
    如 1.4.10 -> 10410
    """
    try:
        versionlist = versionstr.split(".")
        return int(versionlist[0])*10000+int(versionlist[1])*100+int(versionlist[2])
    except Exception as e:
        print(e)
        return -1

class VersionInfo:
    def __init__(self):
        self.has_new_version = False
        self.msg = "No new version"
        self.version_str = ""
        self.update_zip_url = ""
        

def file_checksum(file_path):
    """计算文件的 SHA256 哈希值"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b''):
            sha256.update(block)
    return sha256.hexdigest()

def zip_file_checksum(zip_file, file_in_zip):
    """计算压缩包内文件的 SHA256 哈希值"""
    sha256 = hashlib.sha256()
    with zip_file.open(file_in_zip) as f:
        for block in iter(lambda: f.read(4096), b''):
            sha256.update(block)
    return sha256.hexdigest()
        
def whether_has_new_version():
    """
    检查是否有新版本
    """
    urls = {
        "gitee": "https://gitee.com/api/v5/repos/sammusen/BAAH/releases/latest",
        "github": "https://api.github.com/repos/sanmusen214/BAAH/releases/latest"
    }
    
    eachtime = {}
    eachnewesttag = {} # 存放各个平台上最新的版本号 如 1.5.3
    eachdownloadurl = {} # 存放各个平台上最新的下载链接
    print("Checking for new version...")
    for key in urls:
        nowtime = time.time()
        try:
            print(f"Checking: {key}...")
            response = requests.get(urls[key], timeout=5)
            if response.status_code == 200:
                eachtime[key] = time.time() - nowtime
                data = response.json()
                eachnewesttag[key] = data["tag_name"].replace("BAAH", "")
                eachdownloadurl[key] = [each["browser_download_url"] for each in data["assets"]]
        except Exception as e:
            print(f"Error accessing {key}: {e}")
            continue
    
    if not eachtime:
        print("Failed to check time spent for accessing github nor gitee.")
        vi = VersionInfo()
        vi.msg = "Failed to check time spent for accessing github nor gitee."
        return vi
    print(eachtime)
    print(eachnewesttag)
    fastestkey = min(eachtime, key=eachtime.get)
    newest_tag = eachnewesttag[fastestkey]
    
    # 这里读取software_config.json实际存储的字符串
    # DATA/CONFIGS/software_config.json里的NOWVERSION字段
    with open(os.path.join("DATA", "CONFIGS", "software_config.json"), "r", encoding="utf-8") as f:
        confile = json.load(f)
    current_version_num = get_one_version_num(confile["NOWVERSION"])
    new_version_num = get_one_version_num(newest_tag)
    
    if new_version_num > current_version_num:
        vi = VersionInfo()
        vi.has_new_version = True
        vi.msg = f"New version available: {newest_tag} ({fastestkey})"
        vi.version_str = newest_tag
        vi.update_zip_url = next((url for url in eachdownloadurl[fastestkey] if url.endswith("_update.zip")), "")
        # 如果没有以update末尾的文件，说明没有更新文件
        if vi.update_zip_url == "":
            vi.msg += "\nFailed to get the download URL."
            vi.has_new_version = False
        return vi
    else:
        vi = VersionInfo()
        vi.msg = "No new version"
        return vi
        
def check_and_update():
    # 判断路径下是否有BAAH.exe，如果没有说明运行目录不对
    if not os.path.exists("BAAH.exe"):
        print("Please run this script in the same directory as BAAH.exe.")
        return
    
    version_info = whether_has_new_version()
    # 如果没有新版本，直接返回
    if not version_info.has_new_version:
        print("No new version available.")
        print(version_info.msg)
        return
    # 根据update.zip结尾的url下载文件
    target_url = version_info.update_zip_url
    targetfilename = os.path.basename(target_url)
    print("Downloading...Please wait")
    # 不存在zip文件则下载
    if not os.path.exists(targetfilename):
        try:
            response = requests.get(target_url, stream=True, timeout=10)
            if response.status_code == 200:
                block_size = 102400 # B
                total_size = int(response.headers.get('content-length', 0)) # B
                print("total_size: ", total_size/1024, "kB")
                now_size = 0 # B
                with open(targetfilename, "wb") as f:
                    for data in response.iter_content(block_size):
                        f.write(data)
                        # 保留两位小数
                        now_size += block_size
                        print(f"\r{now_size/total_size:.2%}".ljust(10), end="")
                    print("")
                print("Downloading update zip: Success")
            else:
                print("Downloading update zip: Failed (not 200)")
                return
        except Exception as e:
            print("Downloading new version: Failed")
            print(f"Error downloading file: {e}")
            raise Exception("Failed to download the ZIP file.")
    else:
        print(f"Update ZIP file: {targetfilename} already exists.")
    
    # Check and terminate BAAH.exe and BAAH_GUI.exe processes
    # 中断已有的BAAH进程
    processes_to_terminate = ["BAAH.exe", "BAAH_GUI.exe"]
    for process in processes_to_terminate:
        try:
            #! only for Windows now
            # Windows，未来多平台可以考虑使用psutil库
            subprocess.run(f'taskkill /f /im {process}', shell=True, check=True)
            print(f"Terminated process: {process}")
        except subprocess.CalledProcessError as e:
            # but thats fine, maybe it is not running
            print(f"Failed to terminate process {process}: {e}")
    # 之后重新启动GUI
    global open_GUI_again
    open_GUI_again = True
    # Extract the downloaded ZIP file
    # 解压下载下来的zip文件
    try:
        # zip第一层是一个BAAH1.5.4这样的大文件夹，跳过
        total_sub_files_extracted = 0
        with zipfile.ZipFile(targetfilename, 'r') as zip_ref:
            all_files = zip_ref.namelist()
            # 把BAAH_UPDATE.exe放到最后
            file_updateexe_name = next((file for file in all_files if file.endswith("BAAH_UPDATE.exe")), None)
            if file_updateexe_name:
                all_files.remove(file_updateexe_name)
                all_files.append(file_updateexe_name)
            for file in all_files:
                if file.endswith("/"):
                    # 文件夹不作为文件处理
                    continue
                if file.startswith(f"BAAH{version_info.version_str}/"):
                    # 去除第一层文件夹
                    relative_path = os.path.relpath(file, f"BAAH{version_info.version_str}/")
                    # 如果有深层文件夹，创建深层文件夹
                    os.makedirs(os.path.dirname(relative_path), exist_ok=True) if os.path.dirname(relative_path) else None
                    # 判断文件是否存在
                    if os.path.exists(relative_path):
                        # 如果存在，检查hash是否一致
                        src_hash = zip_file_checksum(zip_ref, file)
                        dst_hash = file_checksum(relative_path)
                        # print(f"src_hash: {src_hash}, dst_hash: {dst_hash}")
                        if src_hash == dst_hash:
                            continue
                        else:
                            print(f"detected file change: {relative_path}")
                    else:
                        print(f"file not exists: {relative_path}, write it.")
                    print(f"    Extracting {file} to {relative_path}")
                    # 解压文件到relative_path，覆盖
                    with zip_ref.open(file) as zf, open(relative_path, "wb") as f:
                        shutil.copyfileobj(zf, f)
                        total_sub_files_extracted += 1
                else:
                    print(f"Skipped {file}, this is not start with BAAH{version_info.version_str}/ in zip")
        print(f"\nUpdate successful, {total_sub_files_extracted} files extracted.\n")
    except zipfile.BadZipFile:
        raise Exception("Failed to extract the ZIP file. Bad ZIP file.")
        
        
    # 删除下载的zip文件
    os.remove(targetfilename)
    print(f"Deleted the downloaded ZIP file: {targetfilename}.")

open_GUI_again = False

def main():
    try:
        is_update_file = copy_to_temp_and_run()
        if not is_update_file:
            # 如果是temp，执行check_and_update
            check_and_update()
            print("========== [UPDATE SUCCESS] =========")
        else:
            # 如果是update本体，直接退出，让temp执行
            return
    except Exception as e:
        traceback.print_exc()
        print("========== [ERROR!] =========")
        if "BAAH_UPDATE.exe" in str(e) and "Permission denied" in str(e):
            print(">>> You can not use this script to replace itself. Please unpack the zip manually. <<<")
    
    # 重新启动BAAH_GUI.exe
    # 注意这里CREATE_NEW_CONSOLE即使把本文件命令行窗口关了，也不会影响BAAH_GUI.exe的运行
    if open_GUI_again:
        try:
            # Windows only
            subprocess.Popen(["BAAH_GUI.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
            print("BAAH_GUI.exe started.")
        except Exception as e:
            print(f"Failed to start BAAH_GUI.exe: {e}")

    input("Press Enter to exit: ")


if __name__ == "__main__":
    main()
