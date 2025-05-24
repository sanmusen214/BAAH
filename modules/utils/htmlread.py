import re
import requests

def htmlread(url):
    if "html://" not in url:
        raise Exception("url must start with html://")
    html = requests.get(url.replace("html://", "")).text
    apk_links = re.findall(r'https://pkg.bluearchive-cn.com[^\s\'"]+?\/com.RoamingStar.BlueArchive.apk', html)
    return apk_links[0]