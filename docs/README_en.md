# Blue_Archive_ArisHelper(BAAH)

<div style="display:flex;justify-content:space-around"><img src="../DATA/assets/aris.png" style="width:48%"/><img src="../DATA/assets/kei.png" style="width:48%"/></div>

---

## Discussion Group

QQ: 715586983

Discord: https://discord.com/invite/7cEvvfcd

# How to Run

[Latest Tutorial on Bilibili Homepage](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

## Pre-run Setup

1. Emulator: Set the resolution to 1280*720 pixels, 240 DPI. Enable adb debugging. Note the adb debugging port of the emulator.
   - If you are using Mumu emulator, please disable background activity running at the bottom of the settings.
2. BA Game Settings:
   - Game: Turn off skill animations;
   - Graphics: Set to low resolution; Turn off black bars at the top and bottom during battles,
   - In the café, manually adjust the camera angle to the highest and stack all furniture on the right side of the screen if possible.

## Usage

### Running via exe (Windows)

1. Download and extract the approximately 100MB zip file to any folder.
2. Rename the example.json file in the BAAH_CONFIGS folder to any other name, such as task.json.
3. Double-click BAAH_GUI.exe to open the interface.
4. After modifying the task content of a configuration file in the interface, click `Save and Execute` in the bottom right corner of the interface.

### Running via local Python environment

1. Ensure your Python environment version is >= 3.10.
2. Ensure adb.exe is available on your computer, and later modify the ADB_PATH in the configuration file to point to adb.exe on your computer.
3. Execute `git clone https://github.com/sanmusen214/BAAH.git` in the command line.
4. Execute `cd BAAH` to enter the project directory.
5. Execute `pip install -r requirements.txt` to install the required dependencies.
6. Execute `python jsoneditor.py` to run the GUI, and modify the path to adb.exe at the bottom of the GUI.
7. Execute `python main.py config.json` to start executing BAAH according to the config.json configuration.

### Running via Docker

1. Ensure you have a docker environment
2. You can run in the following ways:
   - Local compilation through `git clone https://github.com/sanmusen214/BAAH.git` and then execute `docker compose up -d`. (If you don't have a suitable network environment, you can uncomment the `dockerfile: Dockerfile.CN` line in the `docker-compose.yml` file)
   - Get the image built by [Github Action](https://github.com/sanmusen214/BAAH/actions) and execute `docker run -d --name BAAH -p 8000:8000 ghcr.io/sanmusen214/baah:latest`, or use the following `docker-compose.yml` file, execute `docker compose up -d`

```yaml
services:
  baah:
    image: ghcr.io/sanmusen214/baah:latest
    volumes:
      - ./BAAH_CONFIGS:/app/BAAH_CONFIGS
    environment:
      - TZ=Asia/Shanghai
      - HOST=0.0.0.0
      - PORT=8000
      # - TOKEN=YOUR_TOKEN
    ports:
      - 8000:8000
```

# FAQs

## 0. How to Update BAAH

Download BAAH1.x.xx_update.zip on [Github releases](https://github.com/sanmusen214/BAAH/releases/) or by clicking the update button in the GUI, then extract all contents to overwrite the existing files in the BAAH folder.

Or just double click `UPDATE.exe` to update BAAH.

## 1. How to Provide Feedback

Please:

0. Check if the issue is already listed in the FAQs.
1. Check whether the BAAH is the latest version. You can update BAAH through the update button in the GUI.
2. Describe your game server, BAAH version.
3. Describe your purpose.
4. Describe the behavior of BAAH before and after the error occurred or provide a recording.
5. Provide logs of BAAH.exe before and after the error occurred.

## 2. ADB Connection Failed, Screenshot Size is 0kb, or Game Continuously Detected as Not Opened

Please check if the adb port number in your configuration file matches the adb port number of the emulator.

Please verify if your server selection in the configuration file is correct.

## 3. How to View the ADB Port Number of Mumu Emulator

Click the three horizontal lines in the upper right corner of the emulator, open problem detection, scroll to the bottom, and the adb port number will be displayed.

## 4. How to View the Port Number of LDPlayer Emulator

You can click the `using serial number` box on the right side of the adb port input box when connecting to the LDPlayer emulator, then enter `emulator-5554`, or try `emulator-5556`, `emulator-5558`, etc., until the connection is successful.

Click Multi-player on the right side of the emulator to find out the current emulator's ID number. The port number is: 5555 + ID * 2.

## 5. If I Installed Anti-Censorship for CN Server BA, BAAH Can't Click the Sweep Button

Please check the "If anti-censorship is enabled, please check this option" box when selecting the server.

## 6. When Using Swipe to Select Levels, the Swipe Distance is Not Enough

This issue usually occurs in CN server official BAs. Unbind the swipe trigger distance from the server in the configuration file and change 40 to 60.

## 7. Can BAAH be Multi-opened?

Switch to different configuration files in the GUI interface, then click Save and Run in the bottom right corner separately.

BAAH can be run through the command line, just cd to the BAAH folder, and execute `BAAH.exe your_config.json`. By combining the Windows Task Scheduler, you can run BAAH automatically at a specific time.

If you are using a bat command or Windows Task Scheduler, make sure to cd to the BAAH folder, then execute `BAAH.exe config1.json` followed by `BAAH.exe config2.json`.

## 8. Can BAAH be Run Multi-opened with Other Scripts?

BAAH is compatible with ALAS and MAA, but:

1. Please do not attempt to run BAAH and ALAS or MAA on the same multi-opened emulator/same emulator port simultaneously, as they will compete for screenshots. Please set up multiple multi-opened emulators.
2. Please be careful not to let the automation scripts restart the adb service, BAAH will not try to shut down the adb daemon, you should start BAAH after other automation tools.

## 9. After Extracting, BAAH.exe Disappears

Please set the BAAH folder as an exception in your antivirus software, then extract it again. BAAH is completely open source.
