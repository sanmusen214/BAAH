import json
import requests

def jsonread(url):
    """
    从url中获取json数据
    tips,原本想让定位也写在url中的，但是不会写。 ——By BlockHaity
    """
    if "json://" not in url:
        return Exception("url must start with json://")
    url = url.replace("json://", "")
    jsondata = json.loads(requests.get(url).text)
    return jsondata['data']['android_download_link']