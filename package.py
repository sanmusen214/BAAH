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
        
def package_create_folder(path):
    try:
        os.mkdir(path)
    except Exception as e:
        print(f"{path}创建时出错!")

def package_remove_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print(f"{path}删除时出错!")

def package_remove_folder(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"{path}删除时出错!")

# ====================开始====================

config_version = config.NOWVERSION

package_remove_file(f"./dist/BAAH{config_version}.zip")
package_remove_file(f"./dist/BAAH{config_version}_update.zip")
package_rename(f"./dist/BAAH{config_version}", f"./dist/BAAH")

# 打包main.py，名字为BAAH
baahcmd = [
    'pyinstaller',
    'main.py',
    '-n', 'BAAH',
    '--icon', './DATA/assets/kei.ico',
    '-y'
]
subprocess.call(baahcmd)

# 打包GUI
guicmd = [
    'pyinstaller',
    'jsoneditor.py',
    # '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--icon', './DATA/assets/aris.ico',
    '-y'
]
subprocess.call(guicmd)


# 当前目录
print("当前目录：", os.getcwd())
workdir = os.getcwd()

print("开始封装")


# 遍历./dist/jsoneditor/_internal里的所有文件夹和文件，将它们拷贝到./dist/BAAH/_internal，如果已存在则跳过
for dirpath, dirnames, filenames in os.walk(os.path.join('./dist', 'jsoneditor', '_internal')):
    for filename in filenames:
        package_copyfile(os.path.join(dirpath, filename), os.path.join('./dist/BAAH/_internal', filename))
    for dirname in dirnames:
        package_copyfolder(os.path.join(dirpath, dirname), os.path.join('./dist/BAAH/_internal', dirname))
    # 走一层就终止
    break

package_copyfolder('./tools/adb', './dist/BAAH/tools/adb')
package_copyfolder('./tools/pponnxcr', './dist/BAAH/_internal/pponnxcr')
package_copyfolder("./DATA/i18n", "./dist/BAAH/DATA/i18n")

package_create_folder("./dist/BAAH/DATA/CONFIGS")
# 将LICENSE挪进去占位, 不放software.config, 防止覆盖掉用户的
package_copyfile("./LICENSE", "./dist/BAAH/DATA/CONFIGS/LICENSE")

package_copyfolder("./BAAH_CONFIGS", "./dist/BAAH/BAAH_CONFIGS")

package_copyfolder("./DATA/assets", "./dist/BAAH/DATA/assets")
package_copyfolder("./DATA/assets_jp", "./dist/BAAH/DATA/assets_jp")
package_copyfolder("./DATA/assets_cn", "./dist/BAAH/DATA/assets_cn")
package_copyfolder("./DATA/assets_global_en", "./dist/BAAH/DATA/assets_global_en")
package_copyfile("./dist/jsoneditor/jsoneditor.exe", "./dist/BAAH/jsoneditor.exe")

# package_rename("./dist/BAAH/BAAH.exe", f"./dist/BAAH/BAAH{config_version}.exe")
package_rename("./dist/BAAH/jsoneditor.exe", f"./dist/BAAH/BAAH_GUI{config_version}.exe")
package_rename("./dist/BAAH", f"./dist/BAAH{config_version}")

print("开始压缩")

# 压缩./dist/BAAH文件夹为BAAH.zip
z = zipfile.ZipFile(f'./dist/BAAH{config_version}.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config_version}"
for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        # 跳过config.json
        if "config.json" in filename:
            continue
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包./dist/BAAH{config_version}.zip已生成")

# 压缩./dist/BAAH文件夹(除了_internal, tools)为BAAH_update.zip
z = zipfile.ZipFile(f'./dist/BAAH{config_version}_update.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/BAAH{config_version}"
for dirpath, dirnames, filenames in os.walk(startdir):
    if "_internal" in dirpath or "tools" in dirpath:
        continue
    for filename in filenames:
        # 跳过config.json
        if "config.json" in filename:
            continue
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包./dist/BAAH{config_version}_update.zip已生成")
