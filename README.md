# Blue_Archive_ArisHelper(BAAH)

BAAH 可以帮助各位sensei在安卓模拟器内完成碧蓝档案（国际服）里的 **每日任务**.

BAAH can help sensei complete daily tasks of Blue Archive (Global ver.) in Android Emulator.

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

## 打算开发/已开发完成的自动化任务:

- [x] 登录游戏相关
  - [x] 跳过活动弹窗
  - [x] 从PV页面登录
  - [x] 关闭社群弹窗

- [x] 咖啡馆相关
  - [x] 领取体力
  - [x] 邀请学生
  - [x] 摸头
- [x] 课程表相关
  - [x] 完成多个课程
- [x] 社团相关
  - [x] 领取体力
- [ ] 制造室相关
  - [ ] 制造
  - [ ] 合成
- [ ] 购买相关
  - [ ] 物品购买
  - [ ] 体力购买

- [x] 主线关卡相关
  - [x] 普通Quest扫荡
  - [x] 困难Quest扫荡
- [x] 活动关卡相关
  - [x] 活动Quest扫荡
- [x] 悬赏通缉相关
  - [x] 悬赏通缉扫荡
- [x] 学园交流会相关
  - [x] 学园交流会扫荡
- [x] 战术大赛相关
  - [x] 挑战一次
  - [x] 领取奖励
- [x] 邮件领取相关
  - [x] 一件领取所有邮件
- [x] 每日任务奖励相关
  - [x] 领取所有
  - [x] 领取20钻石

# 如何运行

## 运行前请确保

1. 将模拟器分辨率设置为 1280*720像素， 240 DPI.
2. 将模拟器设置里的的adb调试打开.
3. 国际服BA的语言设置为繁体中文
4. 国际服BA的绘图里的选项全拉到最右边（FPS和渲染加速模式除外）。
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

# 配置项目

在 `config.py` 中:

1. ADB_PATH: 安卓调试工具adb.exe所在路径
2. TARGET_EMULATOR_PATH：模拟器所在路径
3. TARGET_PORT: 模拟器adb调试的端口
4. TIME_AFTER_CLICK: 执行点击操作后的等待时间
5. TIMETABLE_TASK: 课程表任务配置. 长度为9的一个列表，列表的第i个元素内部指定那个地点要点击的教室们的下标，所有下标从0开始。
   
   `[[1,2],[2],[],[],[],[],[],[],[]]` 意味着在第一个地点点击第一个和第二个教室，在第二个地点点击第二个教室，其他地点无点击

6. WANTED_HIGHEST_LEVEL: 悬赏通缉的任务配置，一个列表。列表的每个元素都是长度为3的数组，第一位表示地点下标，第二位表示地点里的关卡下标，第三位表示扫荡次数。所有下标从0开始. 每天只会从列表中挑出一个关卡进行扫荡。
   
   `[[1, 9, -1], [2, 9, -1]]` 意味着每天从 [[ 第一个地点的第九个关卡扫荡max次 ]，[ 第二个地点的第九个关卡扫荡max次 ]] 中**挑选一个**来完成。

7. EXCHANGE_HIGHEST_LEVEL: 学园交流会的任务配置，同悬赏通缉的任务配置结构。一个列表。列表的每个元素都是长度为3的数组，第一位表示地点下标，第二位表示地点里的关卡下标，第三位表示扫荡次数。所有下标从0开始. 每天只会从列表中挑出一个关卡进行扫荡。

   `EXCHANGE_HIGHEST_LEVEL = [[1, 2, 3], [2, 2, 2], [3, 3, 3]]` 意味着每天从 [[ 第一个地点的第2个关卡扫荡3次 ]，[ 第二个地点的第2个关卡扫荡2次 ]，[ 第三个地点的第3个关卡扫荡3次 ]] 中**挑选一个**来完成。

8. EVENT_QUEST_LEVEL：扫荡活动关卡，每行是一个数组，每天会挑一行执行，支持混合关卡刷取。比如

```python
  [
    [[10, 5], [11, -1]],
    [[12, -1]]
  ]
```
表示第一天刷取第十关五次，然后刷第十一关max次。第二天刷12关max次。以此循环

9.  QUEST: 扫荡主线关卡，分为HARD和NORMAL，各自是一个数组，每天会挑一个数组内的元素执行，也支持混合关卡刷取。比如NORMAL的数组为例
```python
  [
    [[19,1,5], [20,1,-1]],
    [[20,2,-1]]
  ]
```
表示第一天扫荡第19个地点的第一个关卡5次，然后扫荡第20个地点的第1个关卡max次。第二天扫荡第20个地点的第二个关卡max次。注意这里的关卡是指屏幕从上到下数的第几个关卡，比如普通关卡的第三个地区的第一个关卡是TR-5训练关卡，第二个关卡是3-1，那么如果你想刷取3-1，就应该设置为 [3,2,-1]

# 打包

项目下新建tools文件夹，放入压缩包中的adb，nicegui，pponnxcr文件夹

1. `pyinstaller main.spec`
2. `python package.py`
