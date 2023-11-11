# blue_archive_ArisHelper(BAAH)

BAAH 可以帮助各位sensei在安卓模拟器内完成碧蓝档案（国际服）里的 **每日任务**.

灵感来自以下项目:

1. [BAAuto](https://github.com/RedDeadDepresso/BAAuto): 碧蓝档案国际服自动脚本
2. [MBA](https://github.com/MaaAssistantArknights/MBA): MAA架构的碧蓝档案助手
3. [BAAS](https://github.com/pur1fying/blue_archive_auto_script): 蔚蓝档案简中服自动脚本

本项目使用了以下库: 

1. [tesseract](https://github.com/tesseract-ocr/tesseract): 用于OCR数字识别票卷情况

## 已开发完成的自动化任务:

- [x] 登录游戏相关
  - [x] 跳过活动弹窗
  - [x] 从PV页面登录
  - [x] 关闭社群弹窗

- [x] 咖啡馆相关
  - [x] 领取体力
  - [ ] 邀请学生
  - [x] 摸头
- [x] 课程表相关
  - [x] 完成多个课程
- [x] 社团相关
  - [x] 领取体力
- [ ] 制造室相关
  - [ ] 制造
  - [ ] 合成

- [ ] 主线关卡相关
  - [ ] 普通Quest扫荡
  - [x] 困难Quest扫荡
- [x] 悬赏通缉
  - [x] 悬赏通缉每天扫荡随机一个地点
- [x] 学园交流会
  - [x] 学园交流会每天扫荡随机一个地点
- [x] 战术大赛
  - [x] 挑战一次
  - [x] 领取奖励
- [x] 邮件领取
  - [x] 一件领取所有邮件
- [x] 每日任务奖励
  - [x] 领取所有
  - [x] 领取20钻石

# 如何运行

1. 确保安装了 [python](https://www.python.org/downloads/) >= 3.12 (并且添加到系统环境变量中).
2. 确保安装了 [tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (并且添加到 `config.py`)
3. 确保安装了 [adb](https://developer.android.com/studio/releases/platform-tools) (并且添加到系统环境变量中).
4. 将模拟器分辨率设置为 1280*720像素， 240 DPI.
5. 打开模拟器的adb调试界面.
6. 将BA的语言设置为中文
7. 确保BA的咖啡厅的摄像机拉到了最高.

然后进行以下步骤来安装此项目并运行:

1. 克隆本仓仓库 `git clone https://github.com/sanmusen214/BAAH.git` ,  然后执行 `cd ./BAAH`
2. 运行 `python install -r requirements.txt` 来安装所需的依赖库。
3. 改变 `config.py` 的内容来对关卡扫荡做配置
4. 在模拟器内启动BA
5. 执行 `python main.py`，确保此时BA界面在主页或登录进主页之前

# 配置项目

在 `config.py` 中:

1. TESSERACT_PATH: 图像识别软件tesseract.exe所在的路径
2. TARGET_PORT: 模拟器adb调试的端口
3. TIME_AFTER_CLICK: 执行点击操作后的等待时间
4. TIMETABLE_TASK: 时间表任务配置. 长度为9的一个列表，列表的第i个元素内部指定那个地点要点击的教室们的下标，所有下标从0开始。
   
   `[[0,1],[1],[],[],[],[],[],[],[]]` 意味着在第一个地点点击第一个和第二个教室，在第二个地点点击第二个教室，其他地点无点击

5. WANTED_HIGHEST_LEVEL: 悬赏通缉的任务配置，长度为3的一个列表。列表的每个元素都是长度为3的数组，第一位表示地点下标，第二位表示地点里的关卡下标，第三位表示扫荡次数。所有下标从0开始. 每天只会从列表中挑出一个关卡进行扫荡。
   
   `[[0, 8, -1], [1, 8, -1], [2, 8, -1]]` 意味着每天从 [[ 第一个地点的第九个关卡扫荡max次 ]，[ 第二个地点的第九个关卡扫荡max次 ]，[ 第三个地点的第九个关卡扫荡max次 ]] 中**挑选一个**来完成。

6. EXCHANGE_HIGHEST_LEVEL: 学园交流会的任务配置，同悬赏通缉的任务配置结构。长度为3的一个列表。列表的每个元素都是长度为3的数组，第一位表示地点下标，第二位表示地点里的关卡下标，第三位表示扫荡次数。所有下标从0开始. 每天只会从列表中挑出一个关卡进行扫荡。

   `EXCHANGE_HIGHEST_LEVEL = [[0, 1, 3], [1, 1, 3], [2, 1, 3]]` 意味着每天从 [[ 第一个地点的第九个关卡扫荡3次 ]，[ 第二个地点的第九个关卡扫荡3次 ]，[ 第三个地点的第九个关卡扫荡3次 ]] 中**挑选一个**来完成。
