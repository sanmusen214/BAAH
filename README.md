# Blue_Archive_ArisHelper碧蓝档案爱丽丝助手(BAAH)

<div style="display:flex;justify-content:space-around"><img src="./assets/aris.png" style="width:48%"/><img src="./assets/kei.png" style="width:48%"/></div>


---

BAAH 可以帮助各位sensei在安卓模拟器内完成碧蓝档案（国际服/日服/国服官服/国服B服）里的 **每日任务**.

BAAH can help sensei complete daily tasks of Blue Archive (Global ver./Janpan ver.) in Android Emulator.

[English Document is on the way, but it is a complex work to turn displayed text and suit language in BA to English. For those sensei who use English as their main language may need to wait Christmas holiday]

灵感来自以下项目:

1. [BAAuto](https://github.com/RedDeadDepresso/BAAuto): 碧蓝档案国际服自动脚本
2. [MBA](https://github.com/MaaAssistantArknights/MBA): MAA架构的碧蓝档案助手
3. [BAAS](https://github.com/pur1fying/blue_archive_auto_script): 蔚蓝档案简中服脚本

本项目使用了以下库: 

1. [opencv-python](https://github.com/opencv/opencv): 用于模板匹配
2. [pponnxcr](https://github.com/hgjazhgj/pponnxcr): 用于OCR数字
3. [nicegui](https://github.com/zauberzeug/nicegui): 用于GUI功能

## 交流群

QQ: 441069156

[BAAH使用以及常见问题.docx](https://docs.qq.com/doc/DR1RPaURleGF0ZWFS)

## 致谢

图标来自[@dada008](https://space.bilibili.com/23726244)

感谢群友 [@LLL1997](https://github.com/LLL1997) 整理的日服界面元素的截图

感谢群友 [@子墨](https://space.bilibili.com/11179370)整理的国服界面元素的截图

## 打算开发/已开发完成的自动化任务:

- [x] 登录游戏
  - [x] 跳过活动弹窗
  - [x] 从PV页面登录
  - [x] 关闭社群弹窗

- [x] momotalk
  - [x] 清momotalk里的好感对话

- [x] 咖啡馆
  - [x] 领取体力
  - [x] 邀请学生
  - [x] 摸头
- [x] 课程表
  - [x] 完成多个课程
- [x] 社团
  - [x] 领取体力
- [ ] 制造
  - [ ] 制造
  - [ ] 合成
- [x] 商店
  - [x] 物品购买
  - [x] 体力购买

- [x] 普通关卡
  - [x] 普通Quest扫荡
- [x] 困难关卡
  - [x] 困难Quest扫荡
- [x] 活动关卡
  - [x] 活动Quest扫荡
- [x] 悬赏通缉/指名手配
  - [x] 悬赏通缉扫荡
- [x] 特殊任务/特别依赖
  - [x] 特殊关卡扫荡
- [x] 学园交流会
  - [x] 学园交流会扫荡
- [x] 战术大赛/战术对抗
  - [x] 挑战一次
  - [x] 领取奖励
- [x] 邮件
  - [x] 一件领取所有邮件
- [x] 每日任务
  - [x] 领取所有
  - [x] 领取20钻石

# 如何运行

Bilibili：[首页最新教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

[BAAH使用以及常见问题.docx](https://docs.qq.com/doc/DR1RPaURleGF0ZWFS)

## 运行前请确保

1. 将模拟器分辨率设置为 1280*720像素， 240 DPI.
2. 将模拟器设置里的的adb调试打开.
3. 国际服/BA的语言设置为繁体中文
4. 国际服/日服BA的设置里的画面相关的绘图里的选项全拉到最右边（FPS和渲染加速模式除外）。
5. BA的咖啡厅的摄像机拉到了最高，最好家具全堆在屏幕最右侧

## 使用方式

### 通过exe运行

1. 解压压缩包
2. 双击GUI.exe运行

### 通过本地的python环境运行

1. 确保你的python版本>=3.10
2. 确保你的电脑中有adb.exe，并修改config.json里的ADB_PATH
3. 在命令行中执行`git clone https://github.com/sanmusen214/BAAH.git`
4. 执行`cd BAAH` 进入项目目录
5. 执行`pip install -r requirements.txt` 安装所需依赖
6. 执行`python jsoneditor.py` 运行GUI
7. 执行`python main.py config.json`按照config.json配置开始执行BAAH

# 每日任务配置项目

[首页最新教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

# 服务器（国际服/日服/国服官服/国服B服）配置

打开GUI后选择区服即可。
如果选择区服后报错，则修改config.json的下方内容

## 日服

```
"PIC_PATH" : "./assets_jp",
"ACTIVITY_PATH" : "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
```

## 国际服（繁中）

```
"PIC_PATH" : "./assets",
"ACTIVITY_PATH" : "com.nexon.bluearchive/.MxUnityPlayerActivity",
```

## 国服官服

```
"PIC_PATH" : "./assets_cn",
"ACTIVITY_PATH" : "com.RoamingStar.BlueArchive/com.yostar.sdk.bridge.YoStarUnityPlayerActivity",
```

## 国服B服

```
"PIC_PATH" : "./assets_cn",
"ACTIVITY_PATH" : "com.RoamingStar.BlueArchive.bilibili/com.yostar.sdk.bridge.YoStarUnityPlayerActivity",
```

# 打包

项目下新建tools文件夹，放入压缩包中的tools/adb，_internal/nicegui，_internal/pponnxcr文件夹

1. `python package.py`


# 免责声明

该项目与 Nexon、NEXON Games Co., Ltd. 及其任何附属机构无关。

项目中使用的与 Blue Archive (碧蓝档案) 相关的任何游戏资产和资源均属于相应作者的财产和版权。


# 碎碎念

日常任务还缺个制造

未来可以丢弃的按类判别代码：国服悬赏通缉那三个功能选地区，RaidQuest max次判断
