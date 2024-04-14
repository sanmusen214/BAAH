# 碧蓝档案爱丽丝助手(BAAH)

<div style="display:flex;justify-content:space-around"><img src="../DATA/assets/aris.png" style="width:48%"/><img src="../DATA/assets/kei.png" style="width:48%"/></div>

---

## 交流群

QQ: 441069156

# 如何运行

[Bilibili首页最新教程](https://space.bilibili.com/7331920?spm_id_from=333.1007.0.0)

## 运行前设置

1. 模拟器：分辨率设置为 1280*720像素， 240 DPI。将adb调试打开。注意模拟器的adb调试端口号。
   - 如果你使用的Mumu模拟器，请在设置的底部关闭后台保活运行
2. BA游戏内设置： 
  - 游戏：技能动画关；
  - 画面：分辨率低；战斗时上下黑边关，
  - 咖啡厅的摄像机视角手动拉到了最高，最好家具全堆在屏幕最右侧

## 使用方式

### 通过exe运行（Windows）

1. 下载约100MB的压缩包后解压至任意文件夹
2. 将BAAH_CONFIGS文件夹内的example.json重命名为任一其他名字，如task.json
3. 双击BAAH_GUI.exe打开界面
4. 在界面中修改某一配置文件的任务内容后，点击界面右下角的`保存并执行`

### 通过本地的python环境运行

1. 确保你的python环境版本>=3.10
2. 确保你的电脑中有adb.exe，并稍后修改配置文件里的ADB_PATH使其指向你电脑中的adb.exe
3. 在命令行中执行`git clone https://github.com/sanmusen214/BAAH.git`
4. 执行`cd BAAH` 进入项目目录
5. 执行`pip install -r requirements.txt` 安装所需依赖
6. 执行`python jsoneditor.py` 运行GUI，请在GUI的底部修改adb.exe的路径
7. 执行`python main.py config.json`将会按照config.json配置开始执行BAAH

# 常见问题

## 0. 如何更新BAAH

下载 BAAH1.x.xx_update.zip后，解压缩所有内容至BAAH文件夹内覆盖即可。

## 1. 如何反馈

请：

0. 检查问题是否已经列在常见问题里
1. 描述你的游戏区服，BAAH版本号
2. 描述你的目的
3. 描述BAAH在错误发生前后的行为或提供录屏
4. 提供BAAH.exe发生错误前后的日志

## 2. 提示adb连接失败，截图大小为0kb 或 一直检测到游戏未打开，尝试打开游戏

请检查你配置文件里的adb端口号是否和模拟器的adb端口号相同。

清检查你配置文件里的区服选择是否正确。

## 3. 如何查看MUMU模拟器的端口号

点击模拟器右上角三条横线，点开问题检测，滑动到底部，会显示 adb端口号

## 4. 如何查看雷电模拟器的端口号

模拟器右侧点击多开，可以得知当前模拟器的ID编号，端口号为：5555+ID*2

## 5. 国服BA如果自己安装了反和谐，点击不了扫荡按钮

请在选择服务器那块勾选上 "如果开启了反和谐，请勾选此项"

## 6. 使用滑动进行选关时，滑动距离不够

这个问题通常出现在国服官服BA上，请把配置文件底部的滑动触发距离取消与区服绑定，并将40改为60

## 7. BAAH能否多开

在GUI界面切换至不同配置文件，分别点击右下角保存并运行即可。

如果你使用bat命令或Windows的任务计划程序，请确保cd到了BAAH文件夹下，然后执行 `BAAH.exe config1.json` 接着执行 `BAAH.exe config2.json`

## 8. BAAH能否与其他脚本多开

BAAH与ALAS，MAA兼容，只是：

1. 请不要尝试在 一个多开模拟器/一个模拟器端口 上同时运行（BAAH）和（ALAS）或（MAA），他们会抢占截图。请设置多个多开模拟器
2. 请注意尽量不要让自动化脚本重启adb服务

## 9. 解压后BAAH.exe消失了

请将BAAH所在文件夹设置为杀毒软件的白名单重新解压，BAAH完全开源
