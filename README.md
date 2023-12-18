# Blue_Archive_ArisHelper(BAAH)

BAAH 可以帮助各位sensei在安卓模拟器内完成碧蓝档案（国际服/日服）里的 **每日任务**.

BAAH can help sensei complete daily tasks of Blue Archive (Global ver./Janpan ver.) in Android Emulator.

[English Document is on the way, but it is a complex work to turn displayed text and suit language in BA to English. For those sensei who use English as their main language may need to wait Christmas holiday]

灵感来自以下项目:

1. [BAAuto](https://github.com/RedDeadDepresso/BAAuto): 碧蓝档案国际服自动脚本
2. [MBA](https://github.com/MaaAssistantArknights/MBA): MAA架构的碧蓝档案助手
3. [BAAS](https://github.com/pur1fying/blue_archive_auto_script): 蔚蓝档案简中服脚本

本项目使用了以下库: 

1. [opencv-python](https://github.com/opencv/opencv): 用于模板匹配
2. [pponnxcr](https://github.com/hgjazhgj/pponnxcr): 用于OCR数字
3. [nicegui](https://github.com/zauberzeug/nicegui): 用于未来的GUI功能

## 交流群

QQ: 441069156

## 致谢

感谢群友 [LLL1997](https://github.com/LLL1997) 整理的日服界面元素的截图

## 打算开发/已开发完成的自动化任务:

- [x] 登录游戏
  - [x] 跳过活动弹窗
  - [x] 从PV页面登录
  - [x] 关闭社群弹窗

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
- [ ] 商店
  - [ ] 物品购买
  - [ ] 体力购买

- [x] 普通关卡
  - [x] 普通Quest扫荡
- [x] 困难关卡
  - [x] 困难Quest扫荡
- [x] 活动关卡
  - [x] 活动Quest扫荡
- [x] 悬赏通缉
  - [x] 悬赏通缉扫荡
- [x] 特殊任务
  - [x] 特殊关卡扫荡
- [x] 学园交流会
  - [x] 学园交流会扫荡
- [x] 战术大赛
  - [x] 挑战一次
  - [x] 领取奖励
- [x] 邮件
  - [x] 一件领取所有邮件
- [x] 每日任务
  - [x] 领取所有
  - [x] 领取20钻石

# 如何运行

Bilibili：[首页最新教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

## 运行前请确保

1. 将模拟器分辨率设置为 1280*720像素， 240 DPI.
2. 将模拟器设置里的的adb调试打开.
3. 国际服/日服BA的语言设置为繁体中文
4. 国际服/日服BA的绘图里的选项全拉到最右边（FPS和渲染加速模式除外）。
5. BA的咖啡厅的摄像机拉到了最高，最好家具全堆在屏幕最右侧

## 使用方式

### 通过exe运行

1. 解压压缩包
2. 修改config.json
3. 双击BAAH.exe运行

### 通过本地的python环境运行

1. 确保你的python版本>=3.10
2. 确保你的电脑中有adb.exe，并修改config.json里的ADB_PATH
3. 在命令行中执行`git clone https://github.com/sanmusen214/BAAH.git`
4. 执行`cd BAAH` 进入项目目录
5. 执行`pip install -r requirements.txt` 安装所需依赖
6. 修改config.py
7. 执行`python main.py` 运行BAAH

# 每日任务配置项目

[首页最新教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

# 服务器（国际服/日服/国服）配置

## 日服

config.json末尾的PIC_PATH和ACTIVITY_PATH修改为：

```
"PIC_PATH" : "./assets_jp",
"ACTIVITY_PATH" : "com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity",
```

## 国际服

config.json末尾的PIC_PATH和ACTIVITY_PATH修改为：
```
"PIC_PATH" : "./assets",
"ACTIVITY_PATH" : "com.nexon.bluearchive/.MxUnityPlayerActivity",
```

## 国服（未来版本实现）

config.json末尾的PIC_PATH和ACTIVITY_PATH修改为：
```
"PIC_PATH" : "./assets_cn",
"ACTIVITY_PATH" : "com.RoamingStar.BlueArchive/com.yostar.sdk.bridge.YoStarUnityPlayerActivity",
```

# 更新记录

## 1.0.5

1. 修复日服相关bug
2. 支持第二咖啡厅，支持日服神明文字活动扫荡
3. 支持多次战术大赛挑战，在config.json的TASK_ORDER里写多次"战术大赛"即可
4. 优化咖啡厅领取逻辑
5. 优化选关逻辑

## 1.0.4

1. 添加日服支持（神明文字活动关卡扫荡暂不支持，需等待下个版本或下下个版本更新）

## 1.0.3

1. 添加特殊关卡扫荡功能
2. 设置中添加 max-n 次扫荡次数

## 1.0.2

1. 初步修复了adb命令未指定设备导致的截图失效以及无限尝试打开ba的问题
2. 从config.json中解离版本号

## 1.0.1

1. 初始版本

# 打包

项目下新建tools文件夹，放入压缩包中的adb，nicegui，pponnxcr文件夹

1. `pyinstaller main.spec`
2. `python package.py`


# 碎碎念

由于增加了对日服的支持，现在需要考虑账号config分离的问题。理想情况是通过参数化TASK_ORDER里的元素。

GUI虽然个人感觉不是很重要，但是改config也不能老是到记事本里面改，有空再做个前端。目前先把基础功能完善了。不过制造的优先级判断太麻烦了实在不想写，购买也需要注意安全性，别一不小心给别人钻石花光了。
