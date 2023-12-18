import zipfile
import shutil
import os
from modules.utils.MyConfig import config
import subprocess
from pathlib import Path
import nicegui

# 清空dist文件夹
try:
    shutil.rmtree('./dist')
    print("dist文件夹已删除")
except FileNotFoundError as e:
    print("dist文件夹不存在!跳过删除")

# 打包BAAH
baahcmd = [
    'pyinstaller',
    'main.spec'
]
subprocess.call(baahcmd)

# 打包GUI
guicmd = [
    'pyinstaller',
    'jsoneditor.py',
    # '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
]
subprocess.call(guicmd)


# 当前目录
print("当前目录：", os.getcwd())
workdir = os.getcwd()

print("开始封装")

try:
    # 拷贝./tools/adb文件夹到./dist/BAAH/tools/adb
    shutil.copytree('./tools/adb', os.path.join('./dist','BAAH','tools','adb'))
    print("adb文件夹已拷贝")
except FileExistsError as e:
    print("adb文件夹已存在!")
# 遍历./dist/jsoneditor/_internal里的所有文件夹和文件，将它们拷贝到./dist/BAAH/_internal
for dirpath, dirnames, filenames in os.walk(os.path.join('./dist', 'jsoneditor', '_internal')):
    for filename in filenames:
        try:
            shutil.copyfile(os.path.join(dirpath, filename), os.path.join('./dist', 'BAAH', '_internal', filename))
            print(f"{filename}已拷贝")
        except FileExistsError as e:
            continue
    for dirname in dirnames:
        try:
            shutil.copytree(os.path.join(dirpath, dirname), os.path.join('./dist', 'BAAH', '_internal', dirname))
            print(f"{dirname}文件夹已拷贝")
        except FileExistsError as e:
            continue
    # 走一层就终止
    break
print("_internal文件夹已拷贝")
try:
    # 拷贝./tools/pponnxcr文件夹到./dist/BAAH/_internal/pponnxcr
    shutil.copytree('./tools/pponnxcr', os.path.join('./dist','BAAH','_internal','pponnxcr'))
    print("pponnxcr文件夹已拷贝")
except FileExistsError as e:
    print("pponnxcr文件夹已存在!")
try:
    # 拷贝./config.json到./dist/BAAH/config.json
    shutil.copyfile('./config.json', os.path.join('./dist', 'BAAH', 'config.json'))
    print("config.json已拷贝")
except FileExistsError as e:
    print("config.json已存在!")
try:
    # 拷贝./重启adb服务.bat到./dist/BAAH/重启adb服务.bat
    shutil.copyfile('./重启adb服务.bat', os.path.join('./dist', 'BAAH', '重启adb服务.bat'))
    print("重启adb服务.bat已拷贝")
except FileExistsError as e:
    print("重启adb服务.bat已存在!")
try:
    # 拷贝assets文件夹到./dist/BAAH/assets
    shutil.copytree('./assets', os.path.join('./dist', 'BAAH', 'assets'))
    print("assets文件夹已拷贝")
except FileExistsError as e:
    print("assets文件夹已存在!")
try:
    # 拷贝assets_jp文件夹到./dist/BAAH/assets_jp
    shutil.copytree('./assets_jp', os.path.join('./dist', 'BAAH', 'assets_jp'))
    print("assets_jp文件夹已拷贝")
except FileExistsError as e:
    print("assets_jp文件夹已存在!")
try:
    # 拷贝./dist/jsoneditor/jsoneditor.exe到./dist/BAAH/jsoneditor.exe
    shutil.copyfile(os.path.join('./dist', 'jsoneditor', 'jsoneditor.exe'), os.path.join('./dist', 'BAAH', 'jsoneditor.exe'))
    print("jsoneditor.exe已拷贝")
except FileExistsError as e:
    print("jsoneditor.exe已存在!")

try:
    # 重命名./dist/BAAH/BAAH.exe为./dist/BAAH/BAAH{config.NOWVERSION}.exe
    os.rename(os.path.join('./dist', 'BAAH', 'BAAH.exe'), os.path.join('./dist', 'BAAH', f'BAAH{config.NOWVERSION}.exe'))
except Exception as e:
    print(f"BAAH{config.NOWVERSION}.exe已存在!")

try:
    # 重命名./dist/BAAH/jsoneditor.exe为./dist/BAAH/配置修改GUI{config.NOWVERSION}.exe
    os.rename(os.path.join('./dist', 'BAAH', 'jsoneditor.exe'), os.path.join('./dist', 'BAAH', f'配置修改GUI{config.NOWVERSION}.exe'))
except Exception as e:
    print(f"配置修改GUI{config.NOWVERSION}.exe已存在!")

try:
    # 重命名./dist/BAAH/config.json为./dist/BAAH/config_example.json
    os.rename(os.path.join('./dist', 'BAAH', 'config.json'), os.path.join('./dist', 'BAAH', 'config_example.json'))
except Exception as e:
    print("config_example.json已存在!")
    
try:
    # 重命名./dist/BAAH文件夹为./dist/BAAH{config.NOWVERSION}
    os.rename(os.path.join('./dist', 'BAAH'), os.path.join('./dist', f'BAAH{config.NOWVERSION}'))
except Exception as e:
    print(f'BAAH{config.NOWVERSION}已存在!')

print("重命名成功")

# 压缩./dist/BAAH文件夹为BAAH.zip
z = zipfile.ZipFile(f'./dist/BAAH{config.NOWVERSION}.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config.NOWVERSION}"
for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))
        
# 压缩./dist/BAAH文件夹(除了_internal, tools)为BAAH_update.zip
z = zipfile.ZipFile(f'./dist/BAAH{config.NOWVERSION}_update.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config.NOWVERSION}"
for dirpath, dirnames, filenames in os.walk(startdir):
    # 去除./dist/BAAH/_internal, tools
    if "_internal" in dirpath or "tools" in dirpath:
        continue
    for filename in filenames:
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包已生成")
