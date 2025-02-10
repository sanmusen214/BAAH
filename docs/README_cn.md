# 碧蓝档案爱丽丝助手(BAAH)

<div style="display:flex;justify-content:space-around"><img src="../docs/static/aris.png" style="width:48%"/><img src="../docs/static/kei.png" style="width:48%"/></div>

---

## 交流群

QQ: 715586983

Discord: https://discord.com/invite/7cEvvfcd

# 如何运行

[Bilibili首页最新视频教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

## 运行前设置

1. 模拟器：分辨率设置为 1280*720像素， 240 DPI。将adb调试打开。注意模拟器的adb调试端口号。
   - 如果你使用的Mumu模拟器，请在设置的底部关闭后台保活运行
   - 如果adb无法连接，请确认关闭模拟器的网络桥接功能 或 在其他设置中修改adb连接ip。
2. BA游戏内设置： 
   - 游戏：技能动画关；
   - 画面：战斗时上下黑边关，
   - 咖啡厅的摄像机视角手动拉到了最高，最好家具全堆在屏幕最右侧

## 使用方式

### 通过exe运行（Windows）

1. 下载约100MB的压缩包后解压至任意文件夹
2. 将BAAH_CONFIGS文件夹内的example.json重命名为任一其他名字，如task.json
3. 双击BAAH_GUI.exe打开界面
4. 在模拟器设置中，修改端口号为你的模拟器adb调试端口。
5. 在服务器设置中，选择你游玩的ba服务器。
6. 在任务执行顺序设置中，启用任务流或点击快速执行按钮运行任务。

### 通过本地的python环境运行

1. 确保你的python环境版本==3.10.x
2. 确保你的电脑中有adb.exe，并稍后修改配置文件里的ADB_PATH使其指向你电脑中的adb.exe
3. 在命令行中执行`git clone https://github.com/sanmusen214/BAAH.git`
4. 执行`cd BAAH` 进入项目目录
5. 执行`pip install -r requirements.txt` 安装所需依赖
6. 执行`python jsoneditor.py` 运行GUI，请在GUI的底部修改adb.exe的路径
7. 执行`python main.py config.json`将会按照config.json配置开始执行BAAH

### 通过docker运行

确认你有docker环境，可以通过以下几种方式运行：

1. 拉取镜像：通过获取由[Github Action](https://github.com/sanmusen214/BAAH/actions)构建的镜像，执行`docker run -d --name BAAH -p 8000:8000 ghcr.io/sanmusen214/baah:latest`

2. 本地编译：通过 `git clone https://github.com/sanmusen214/BAAH.git`后，使用提供的`docker-compose.yml`文件，执行`docker compose up -d` (如果没有合适网络的环境可以把docker-compose.yml文件中的`dockerfile: Dockerfile.CN`这行的注释取消)

### 通过安卓termux运行（实验性）

参照 [BlockHaity的博客](https://blockhaity.github.io/2025/02/10/BAAH%E5%9C%A8%E9%80%86%E5%A4%A9%E7%8E%AF%E5%A2%83%E4%B8%8B%E7%9A%84%E8%BF%90%E8%A1%8C/)

# 常见问题

## 0. 如何更新BAAH

从[Github Release](https://github.com/sanmusen214/BAAH/releases/)界面或[Gitee Release](https://gitee.com/sammusen/BAAH/releases)界面或QQ群内或通过点击GUI的更新按钮下载 BAAH1.x.xx_update.zip后，解压缩所有内容至BAAH文件夹内覆盖即可。

或者双击目录下的`UPDATE.exe`来更新BAAH。

## 1. 如何反馈

请：

0. 检查问题是否已经列在常见问题里
1. 检查BAAH是否是最新版本，你可以通过GUI内的更新按钮来更新BAAH
2. 描述你的游戏区服，BAAH版本号
3. 描述你的目的
4. 描述BAAH在错误发生前后的行为或提供录屏
5. 提供BAAH.exe发生错误前后的日志

## 2. 提示adb连接失败，截图大小为0kb 或 一直检测到游戏未打开，尝试打开游戏

请检查你配置文件里的adb端口号是否和模拟器的adb端口号相同。

清检查你配置文件里的游戏区服选择是否正确。

## 3. 如何查看MUMU模拟器的端口号

点击模拟器右上角三条横线，点开问题检测，滑动到底部，会显示 adb端口号

## 4. 如何查看雷电模拟器的端口号

连接到雷电模拟器，可以勾选adb端口输入框右侧的`使用序列号`，然后添入`emulator-5554`，或者依次尝试`emulator-5556`, `emulator-5558`等，直到成功连接。

模拟器右侧点击多开，可以得知当前模拟器的ID编号，端口号为：5555+ID*2

## 5. 国服BA如果自己安装了反和谐，点击不了扫荡按钮

请在选择服务器那块勾选上 "如果开启了反和谐，请勾选此项"

## 6. 使用滑动进行选关时，滑动距离不够，导致脚本点击到按钮间的空白处

这个问题通常出现在国服BA上，请把配置文件底部的滑动触发距离取消与区服绑定，并将原先的40改为60。如果原先是60，请尝试改为40

## 7. BAAH能否多开

在GUI界面切换至不同配置文件，分别点击右下角保存并运行即可。

BAAH可以通过命令行使用，请cd到BAAH文件夹下，执行`BAAH.exe 你的配置名.json`即可运行该配置，结合Windows的任务计划程序可以实现自动启动。

如果你使用bat命令，请确保cd到了BAAH文件夹下，然后执行 `BAAH.exe config1.json` 接着执行 `BAAH.exe config2.json`

## 8. BAAH能否与其他脚本多开

BAAH与ALAS，MAA兼容，只是：

1. 请不要尝试在 一个多开模拟器/一个模拟器端口 上同时运行（BAAH）和（ALAS）或（MAA），他们会抢占截图。请设置多个多开模拟器
2. 请注意尽量不要让自动化脚本重启adb服务，BAAH永远不会重启adb服务，你可以把BAAH放在其它自动化工具的后面启动。

## 9. 解压后BAAH.exe消失了

请将BAAH所在文件夹设置为杀毒软件的白名单重新解压，BAAH完全开源，只需确保你的BAAH下载自github release或本文档开头的QQ群内，即可安心使用。

## 10. 如何让BAAH能够定时自动运行

BAAH的本质是一个可以接受参数的应用程序，当我们打开cmd，cd到BAAH文件夹下，执行`BAAH.exe 你的配置名.json`即可运行该配置。在了解了如何使用windows的任务计划程序后（参见视频教程末尾），您就可以使用任务计划程序控制程序的定时自动运行，结合BAAH中的定时开启/关闭模拟器功能，即可做到解放双手完成BAAH的每日任务。

## 11. GUI运行时参数

你可以在GUI启动时指定参数以实现更多设置，比如 "BAAH_GUI.exe --token 123456" 来为GUI页面设置密码。以下是可使用的参数列表

| Param | Desc | Default |
|-|-|-|
| --host | GUI启动时的ip | 127.0.0.1 |
| --port | GUI启动时的端口 | 8000 （自动查找） |
| --token | GUI密码 | None |
| --no-show | 开关，指定时不自动打开浏览器 | |
