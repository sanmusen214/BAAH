from modules.configs.settingMaps import *

# 用户的脚本config里的默认值以及可选值
# 如果用户的config里没有某个值，先看能否用settingMaps里映射出来，如果不能，就用默认值代替
# 注意引用链

# d: default value
# s: selective value
# m: map value
# from: map value的来源key
# map: map value的映射函数

# selective value作为提醒值存在，主要的map映射值应当在settingMaps里

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
    "PUSH_NORMAL_QUEST": {"d":0},
    "PUSH_NORMAL_QUEST_LEVEL": {"d":1},
    "PUSH_HARD_QUEST": {"d":0},
    "PUSH_HARD_QUEST_LEVEL": {"d":1},
    "TASK_ACTIVATE": {"d":[True]},
    # new config in 1.2.x
    "SERVER_TYPE":{
        "d":"GLOBAL",
        "s":["GLOBAL", "GLOBAL_EN", "JP", "CN", "CN_BILI"],
        "m": {
            "from": "ACTIVITY_PATH",
            "map": lambda x: activity2server[x] if x in activity2server else "GLOBAL"
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
             "map" : lambda x: server2pic[x] if x in server2pic else "./DATA/assets"
        }
    },
    "GRID_SOL_PATH":{
      "d":"./DATA/grid_solution"  
    },
    "FANHEXIE":{"d":False},
    "ACTIVITY_PATH":{
        "d":"com.nexon.bluearchive/.MxUnityPlayerActivity",
        "s":[
            "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
            "com.nexon.bluearchive/.MxUnityPlayerActivity",
            "com.RoamingStar.BlueArchive/com.yostar.supersdk.activity.YoStarSplashActivity",
            "com.RoamingStar.BlueArchive.bilibili/com.yostar.supersdk.activity.YoStarSplashActivity"
        ],
        "m":{
            "from": "SERVER_TYPE",
            "map": lambda x: server2activity[x] if x in server2activity else "com.nexon.bluearchive/.MxUnityPlayerActivity",
        }
    },
    "NEXT_CONFIG" : {"d":""},
    "ADB_PATH":{"d":"./tools/adb/adb.exe"},
    "SCREENSHOT_NAME":{
        "d":"screenshot.png"
    },
    "TARGET_IP_PATH":{"d":"127.0.0.1"},
    "TARGET_PORT":{"d":5555},
    "KILL_PORT_IF_EXIST":{"d":False},
    "TIME_AFTER_CLICK":{"d": 0.7},
    "RESPOND_Y":{
        "d": 40,
        "m":{
            "from": "SERVER_TYPE",
            "map": lambda x: server2respond[x] if x in server2respond else 40
        }
    },
    "SHOP_NORMAL_REFRESH_TIME":{"d": 0},
    "SHOP_CONTEST_REFRESH_TIME":{"d": 0},
    "LOCK_SERVER_TO_RESPOND_Y":{"d": True},
    "CAFE_CAMERA_FULL":{"d":True},
    "AUTO_EVENT_STORY_PUSH":{"d":False},
    "EXPLORE_RAINBOW_TEAMS":{"d":False},
    "ENABLE_MAIL_NOTI":{"d":False},
    "CAFE_TOUCH_WAY_DIFF":{"d":False},
    "USE_VPN":{"d":False},
    "VPN_CONFIG":{"d":{
        "VPN_ACTIVITY":"com.github.kr328.clash/com.github.kr328.clash.MainActivity",
        "CLICK_AND_WAIT_LIST":[[(622, 248), 2]],
    }}
}

# 软件的config里的默认值

defaultSoftwareDict = {
    "LANGUAGE":{"d":"zh_CN", "s":["zh_CN", "en_US"]},
    "MAIL_USER":{"d":""},
    "MAIL_PASS":{"d":""},
}

# sessiondict是一个dict，存储了一次任务的运行时信息
defaultSessionDict = {
    "PORT_IS_USED":{"d":False},
    "EMULATOR_PROCESS_PID":{"d":None},
    "GUI_OPEN_IN_WEB":{"d":True},
    "LAST_TEAM_SET":{"d":[]},
    "CAFE_HAD_INVITED":{"d":True},
}