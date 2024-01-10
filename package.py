import zipfile
import shutil
import os
from modules.configs.MyConfig import config
import subprocess
from pathlib import Path
import nicegui

def package_copyfolder(src, dst):
    try:
        # 拷贝文件夹
        shutil.copytree(src, dst)
        print(f"{dst}文件夹已拷贝")
    except FileExistsError as e:
        print(f"{dst}文件夹已存在!")

def package_copyfile(src, dst):
    try:
        shutil.copyfile(src, dst)
        print(f"{dst}已拷贝")
    except FileExistsError as e:
        print(f"{dst}已存在!")

def package_rename(src, dst):
    try:
        os.rename(src, dst)
    except Exception as e:
        print(f"{dst}已存在!")
        



# ====================开始====================
# 清空dist文件夹
try:
    shutil.rmtree('./dist')
    print("dist文件夹已删除")
except FileNotFoundError as e:
    print("dist文件夹不存在!跳过删除")

config_version = config.NOWVERSION

# 打包main.py，名字为BAAH
baahcmd = [
    'pyinstaller',
    'main.py',
    '-n', 'BAAH',
    '--icon', 'assets/kei.ico',
]
subprocess.call(baahcmd)

# 打包GUI
guicmd = [
    'pyinstaller',
    'jsoneditor.py',
    # '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--icon', 'assets/aris.ico',
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

package_copyfolder('./tools/pponnxcr', './dist/BAAH/_internal/pponnxcr')
package_copyfolder("./DATA", "./dist/BAAH/DATA")
package_copyfolder("./BAAH_CONFIGS", "./dist/BAAH/BAAH_CONFIGS")
package_copyfolder("./assets", "./dist/BAAH/assets")
package_copyfolder("./assets_jp", "./dist/BAAH/assets_jp")
package_copyfolder("./assets_cn", "./dist/BAAH/assets_cn")
package_copyfile("./dist/jsoneditor/jsoneditor.exe", "./dist/BAAH/jsoneditor.exe")

package_rename("./dist/BAAH/BAAH.exe", f"./dist/BAAH/BAAH{config_version}.exe")
package_rename("./dist/BAAH/jsoneditor.exe", f"./dist/BAAH/BAAH GUI{config_version}.exe")
package_rename("./dist/BAAH", f"./dist/BAAH{config_version}")

print("开始压缩")

# 压缩./dist/BAAH文件夹为BAAH.zip
z = zipfile.ZipFile(f'./dist/BAAH{config_version}.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config_version}"
for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包./dist/BAAH{config_version}.zip已生成")

# 压缩./dist/BAAH文件夹(除了_internal, tools, BAAH_CONFIGS)为BAAH_update.zip
z = zipfile.ZipFile(f'./dist/BAAH{config_version}_update.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config_version}"
for dirpath, dirnames, filenames in os.walk(startdir):
    if "_internal" in dirpath or "tools" in dirpath or "BAAH_CONFIGS" in dirpath:
        continue
    for filename in filenames:
        if "重启adb服务" in filename:
            continue
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包./dist/BAAH{config_version}_update.zip已生成")
