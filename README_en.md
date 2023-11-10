# blue_archive_ArisHelper(BAAH)

BAAH can help you finish **daily tasks** of Blue Archive(BA, global ver.) automatically in an Android emulater.

This project is inspired by:

1. [BAAuto](https://github.com/RedDeadDepresso/BAAuto): Blue Archive Auto Script. Inspired by MAA for Arknights and Alas for Azur Lane.
2. [MBA](https://github.com/MaaAssistantArknights/MBA): BA assistant in MAA infrastructure.
3. [BAAS](https://github.com/pur1fying/blue_archive_auto_script): Blue archive auto script for BA(CN ver.).

## Tasks developed:

- [x] EnterGame
- [x] InCafe
- [x] InTimeTable
- [x] InClub
- [ ] InCraft

- [ ] InWanted
- [ ] InExchange
- [ ] InContest

- [x] CollectMails
- [x] CollectDailyRewards

# How to run

1. Make sure you have a python >= 3.12 (and add it to the system path).
2. Make sure you have adb installed in the computer (and add it to the system path).
3. Make sure the graphic setting of your Android emulator is 1280*720 pixels with 240 DPI.
4. Make sure you open the adb debugging function of your emulator.
5. Make sure the language of your BA is set to Chinese (traditional). (Other language support is coming, soon? Since there is only picture differences).
6. Make sure the camera of your BA cafe is zoom out to the highest.

Please follow these steps once you reach requirements above:

1. Clone this repo and `cd ./blue_archive_ArisHelper`
2. Run `python install -r requirements.txt` to install all required libraries.
3. Change the `config.py` to do some configuration.
4. Open your emulater and click the icon of the BA
5. Run `python main.py`

# Do some configuration

In `config.py`:

1. TARGET_PORT: the port of your emulator.
2. TIME_AFTER_CLICK: the sleep time of each click, this will also effect the interval of screen shot.
3. TIMETABLE_TASK: The desired timetable clicking. It is a list with length = 9, each element means the classroom of that location. All index start from 0.
