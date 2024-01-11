from modules.configs.settingMaps import *

# 用户的脚本config里的默认值以及可选值
# 如果用户的config里没有某个值，先看能否用settingMaps里映射出来，如果不能，就用这个值代替

# d: default value
# s: selective value
# m: map value

# selective值作为备用提醒存在，主要的map应当在settingMaps里

defaultUserDict = {
    "TIMETABLE_TASK": {"d":[]},
    "WANTED_HIGHEST_LEVEL": {"d":[]},
    "SPECIAL_HIGHTEST_LEVEL": {"d":[]},
    "EXCHANGE_HIGHEST_LEVEL": {"d":[]},
    "EVENT_QUEST_LEVEL": {"d":[]},
    "HARD": {"d":[]},
    "NORMAL": {"d":[]},
    "TASK_ORDER": {"d":["登录游戏"]},
    "SHOP_NORMAL": {"d":[]},
    "SHOP_CONTEST": {"d":[]},
    "TASK_ACTIVATE": {"d":[True]},
    # new config in 1.2.x
    "SERVER_TYPE":{
        "d":"GLOBAL",
        "s":["GLOBAL", "GLOBAL_EN", "JP", "CN", "CN_BILI"],
        "m": {
            "from": "ACTIVITY_PATH",
            "map": lambda x: activity2server[x]
        }
    },
    "TARGET_EMULATOR_PATH":{"d":""},
    "CLOSE_EMULATOR_BAAH":{"d":False},
    "PIC_PATH":{
        "d":"./DATA/assets",
        "s":[
            "./DATA/assets",
            "./DATA/assets_cn",
            "./DATA/assets_jp",
            "./DATA/assets_global_en"
        ],
        "m":{
            "from" : "SERVER_TYPE",
             "map" : lambda x: server2pic[x]
        }
    },
    "FANHEXIE":{"d":False},
    "ACTIVITY_PATH":{
        "d":"",
        "s":[
            "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
            "com.nexon.bluearchive/.MxUnityPlayerActivity",
            "com.RoamingStar.BlueArchive/com.yostar.supersdk.activity.YoStarSplashActivity",
            "com.RoamingStar.BlueArchive.bilibili/com.yostar.supersdk.activity.YoStarSplashActivity"
        ],
        "m":{
            "from": "SERVER_TYPE",
            "map": lambda x: server2activity[x],
        }
    },
    "NEXT_CONFIG" : {"d":""},
    "ADB_PATH":{"d":"./tools/adb/adb.exe"},
    "SCREENSHOT_NAME":{
        "d":"screenshot.png"
    },
    "TARGET_IP_PATH":{"d":"127.0.0.1"},
    "TARGET_PORT":{"d":5555},
    "TIME_AFTER_CLICK":{"d": 0.7},
    "RESPOND_Y":{
        "d": 40,
        "m":{
            "from": "SERVER_TYPE",
            "map": lambda x: server2respond[x]
        }
    },
    "SHOP_NORMAL_REFRESH_TIME":{"d": 0},
    "SHOP_CONTEST_REFRESH_TIME":{"d": 0},
    "LOCK_SERVER_TO_RESPOND_Y":{"d": True},
    "CAFE_CAMERA_FULL":{"d":True}
}

# 软件的config里的默认值

defaultSoftwareDict = {
    "LANGUAGE":{"d":"zh_CN", "s":["zh_CN", "en_US"]}
}