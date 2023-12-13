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

# 重命名./dist/BAAH/BAAH.exe为./dist/BAAH/BAAH{config.NOWVERSION}.exe
os.rename(os.path.join('./dist', 'BAAH', 'BAAH.exe'), os.path.join('./dist', 'BAAH', f'BAAH{config.NOWVERSION}.exe'))

# 重命名./dist/BAAH/config.json为./dist/BAAH/config_example.json
os.rename(os.path.join('./dist', 'BAAH', 'config.json'), os.path.join('./dist', 'BAAH', 'config_example.json'))

# 重命名./dist/BAAH文件夹为./dist/BAAH{config.NOWVERSION}
os.rename(os.path.join('./dist', 'BAAH'), os.path.join('./dist', f'BAAH{config.NOWVERSION}'))

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
