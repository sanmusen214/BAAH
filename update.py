import subprocess
import requests
import os
import zipfile
import time
from modules.configs.MyConfig import config

def check_and_update():
    urls = {
        "gitee": "https://gitee.com/api/v5/repos/sammusen/BAAH/releases/latest",
        "github": "https://api.github.com/repos/sanmusen214/BAAH/releases/latest"
    }
    
    eachtime = {}
    eachnewesttag = {}
    eachdownloadurl = {}
    
    for key in urls:
        nowtime = time.time()
        try:
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
        print("Failed to check for updates.")
        return
    
    fastestkey = min(eachtime, key=eachtime.get)
    newest_tag = eachnewesttag[fastestkey]
    
    current_version_num = config.get_one_version_num()
    new_version_num = config.get_one_version_num(newest_tag)
    
    if new_version_num > current_version_num:
        print(f'New version available: {newest_tag} ({fastestkey})')
        
        target_urls = eachdownloadurl[fastestkey]
        target_url = next((url for url in target_urls if url.endswith("_update.zip")), "")
        
        if not target_url:
            print("Failed to check for updates.")
            return
        
        targetfilename = os.path.basename(target_url)
        if not os.path.exists(targetfilename):
            try:
                response = requests.get(target_url, timeout=10)
                if response.status_code == 200:
                    with open(targetfilename, "wb") as f:
                        f.write(response.content)
                    print("Downloading new version: Success")
                else:
                    print("Downloading new version: Failed")
                    return
            except Exception as e:
                print("Downloading new version: Failed")
                print(f"Error downloading file: {e}")
                return
        
        # Check and terminate BAAH.exe and BAAH_GUI.exe processes
        processes_to_terminate = ["BAAH.exe", "BAAH_GUI.exe"]
        for process in processes_to_terminate:
            try:
                # Windows
                subprocess.run(f'taskkill /f /im {process}', shell=True, check=True)
                print(f"Terminated process: {process}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to terminate process {process}: {e}")
        
        # Extract the downloaded ZIP file
        try:
            os.makedirs(os.path.join("DATA", "update"), exist_ok=True)
            with zipfile.ZipFile(targetfilename, 'r') as zip_ref:
                zip_ref.extractall(os.path.join("DATA", "update"))
            print("Update successful, files extracted.")
            # TODO: Move the extracted files to the root directory
        except zipfile.BadZipFile:
            print("Failed to extract the ZIP file.")
    else:
        print("No new version available.")

check_and_update()