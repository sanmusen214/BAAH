VERSION = "0.3.0"
# ========configuration============ 
TESSERACT_PATH = r"D:\Software\Tesseract\tesseract.exe"
ADB_PATH = r"D:\软件\ADB\adb.exe"
TARGET_PORT = 11762

TIMETABLE_TASK = [[6, 7],[6, 7],[6, 7],[6],[],[],[],[],[]]

WANTED_HIGHEST_LEVEL = [[0, 8, -1], [1, 8, -1], [2, 8, -1]]
EXCHANGE_HIGHEST_LEVEL = [[0, 1, 3], [1, 1, 3], [2, 1, 3]]

QUEST = {
            "HARD":     [
                            [[13,1,3], [16,1,3]],
                            [[13,2,3]],
                        ],
            "NORMAL":   [
                            [[16,1,2], [17,1,2]],
                            [[15,4,2], [18,2,3]],
                        ],
        }

TIME_AFTER_CLICK = 0.7

# =================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TIME_OUT = 60
PIC_PATH = "./assets"
SCREENSHOT_NAME = "screenshot.png"