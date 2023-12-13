import zipfile
import shutil
import os
from modules.utils.MyConfig import config

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
try:
    # 拷贝./tools/nicegui文件夹到./dist/BAAH/_internal/nicegui
    shutil.copytree('./tools/nicegui', os.path.join('./dist','BAAH','_internal','nicegui'))
    print("nicegui文件夹已拷贝")
except FileExistsError as e:
    print("nicegui文件夹已存在!")
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

# 压缩./dist/BAAH文件夹为BAAH.zip
z = zipfile.ZipFile(f'./dist/BAAH{config.VERSION}.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = "./dist/BAAH"
for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        z.write(os.path.join(dirpath, filename))

print(f"完成，压缩包'./dist/BAAH{config.VERSION}.zip'已生成")
