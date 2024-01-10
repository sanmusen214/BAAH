# Blue_Archive_ArisHelper(BAAH)

<div style="display:flex;justify-content:space-around"><img src="../DATA/assets/aris.png" style="width:48%"/><img src="../DATA/assets/kei.png" style="width:48%"/></div>


---

BAAH can help senseis complete daily tasks in Blue Archive (Global/Japanese/Chinese Server/Chinese Bilibili Server) within an Android Emulator on PC.

Inspired by the following projects:

1. [BAAuto](https://github.com/RedDeadDepresso/BAAuto): Automatic script for Blue Archive Global Version
2. [MBA](https://github.com/MaaAssistantArknights/MBA): MAA framework-based Blue Archive Assistant
3. [BAAS](https://github.com/pur1fying/blue_archive_auto_script): Simplified Chinese script for Blue Archive

This project uses the following libraries: 

1. [opencv-python](https://github.com/opencv/opencv): For template matching
2. [pponnxcr](https://github.com/hgjazhgj/pponnxcr): For OCR of numbers
3. [nicegui](https://github.com/zauberzeug/nicegui): For GUI features

## Discussion Group

QQ: 441069156

[BAAH Usage and FAQs (Chinese).docx](https://docs.qq.com/doc/DR1RPaURleGF0ZWFS)

## Acknowledgements

Icon from [@dada008](https://space.bilibili.com/23726244)

Thanks to group member [@LLL1997](https://github.com/LLL1997) for organizing screenshots of the Japanese version interface elements

Thanks to group member [@子墨](https://space.bilibili.com/11179370) for organizing screenshots of the Chinese version interface elements

## Planned/Completed Automated Tasks:

- [x] Log into the game
  - [x] Skip event pop-ups
  - [x] Log in from the PV page
  - [x] Close community pop-ups

- [x] momotalk
  - [x] Clear affection dialogues in momotalk

- [x] Café
  - [x] Claim stamina
  - [x] Invite students
  - [x] Head patting
- [x] Timetable
  - [x] Complete multiple courses
- [x] Club
  - [x] Claim stamina
- [ ] Manufacturing
  - [ ] Manufacture
  - [ ] Synthesize
- [x] Shop
  - [x] Purchase items
  - [x] Purchase stamina

- [x] Normal Stages
  - [x] Sweep normal Quests
- [x] Hard Stages
  - [x] Sweep hard Quests
- [x] Event Stages
  - [x] Sweep event Quests
- [x] Bounty/Wanted
  - [x] Sweep bounty missions
- [x] Special Missions/Special Dependence
  - [x] Sweep special stages
- [x] School Exchange
  - [x] Sweep school exchange
- [x] Tactical Contest/Tactical Confrontation
  - [x] Challenge once
  - [x] Claim rewards
- [x] Mail
  - [x] Claim all mails in one go
- [x] Daily Tasks
  - [x] Claim all
  - [x] Claim 20 diamonds

# How to Run

Bilibili: [Latest Tutorial on Homepage](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

[BAAH Usage and FAQs.docx](https://docs.qq.com/doc/DR1RPaURleGF0ZWFS)

## Before Running, Please Ensure

1. Set the emulator resolution to 1280*720 pixels, 240 DPI.
2. Enable adb debugging in the emulator settings.
3. In the settings of the Global/Japanese version of BA, pull all options in the drawing section of the screen-related settings to the far right (except FPS and rendering acceleration mode).
4. In BA's café, pull the camera to the highest, and it's best to stack all the furniture on the far right of the screen

## How to Use

### Running via exe

1. Unzip the package
2. Double click BAAH_GUI.exe to run

### Running via local python environment

1. Ensure your python version is >=3.10
2. Ensure you have adb.exe on your computer, and modify the ADB_PATH in config.json, or move your adb folder into `./tools/adb`.
3. Execute `git clone https://github.com/sanmusen214/BAAH.git` in the command line
4. Execute `cd BAAH` to enter the project directory
5. Execute `pip install -r requirements.txt` to install necessary dependencies
6. Execute `python jsoneditor.py` to run GUI
7. Execute `python main.py config.json` to start running BAAH according to the configuration in config.json

# Packaging

Create a new tools folder under the project, put the tools/adb, _internal/nicegui, _internal/pponnxcr folders from the package into it

1. `python package.py`


# Disclaimer

This project is not affiliated with Nexon, NEXON Games Co., Ltd., or any of their subsidiaries.

Any game assets and resources related to Blue Archive used in this project are the property and copyright of their respective authors.

# Small Thoughts

Still missing manufacturing in daily tasks

Future discardable code by category: The three functions of the Chinese version's bounty missions to select regions, RaidQuest max times judgement
