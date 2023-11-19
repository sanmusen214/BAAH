import config
import logging
from modules.utils.subprocess_helper import subprocess_run
import time

def connect_to_device():
    """Connect to a device with the given device port."""
    subprocess_run([config.ADB_PATH, "connect", "127.0.0.1:{}".format(config.TARGET_PORT)])
    
def click_on_screen(x, y):
    """Click on the given coordinates."""
    subprocess_run([config.ADB_PATH, "shell", "input", "tap", str(x), str(y)])

def swipe_on_screen(x1, y1, x2, y2, ms):
    """Swipe from the given coordinates to the other given coordinates."""
    subprocess_run([config.ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(int(ms))])
    
def screen_shot_to_file():
    """Take a screenshot and save it to the given file."""
    filename = config.SCREENSHOT_NAME
    subprocess_run([config.ADB_PATH, "shell", "screencap", r"/sdcard/{0}".format(filename)])
    subprocess_run([config.ADB_PATH, "pull", r"/sdcard/{0}".format(filename), "."])
    