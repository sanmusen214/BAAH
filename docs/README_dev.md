# 项目结构

```
- BAAH_CONFIGS/ 用户配置的需要执行的任务
- DATA/ 此项目所需的各类静态资源以及多语言支持
- docs/ 文档
- gui/ 一个config相关的用户界面
  |-components/ 可复用组件
  |-pages/ 页面以及子页面
  |-__init__.py 对于一个config而言的编辑页面
- modules/ 主要模块
  |- AllPage/ 定义了Page类，通常与页面级别的定位有关
  |- AllTask/ 定义了Task类，通常与某一项每日任务有关
  |- configs/ 定义了MyConfigger类，与此项目所需的各种config操作有关
  |- utils/ 定义了工具类，涉及到adb与图像操作
- tools/ 被调用的adb以及库的静态资源包，注意这些资源不在github里面
  |- adb/
  |- nicegui/
  |- pponnxcr/
- BAAH.py 执行某一个用户配置的任务文件
- jsoneditor.py 为gui的入口文件
- main.py 为主程序的入口文件
- requirements.txt 所有依赖
```

# 项目运行

自动脚本项目从main.py作为入口，从命令行读取用户指定的用户配置文件，然后通过AllTask下的myAllTask类解析此用户配置文件的每日任务，为每个任务创建相应的Task实例为一个列表，在BAAH.py里按序运行这些Task实例。

# 项目打包

使用pyinstaller打包，打包命令为

```python
python package.py
```

# 关键类

## modules/configs/Configger类

位于modules/configs/下的MyConfig控制了用户配置文件的内容，其关键行为是给未出现的用户配置文件赋默认值，以及通过已知的配置推算未知的配置。这两个功能分别和settingMaps.py和defaultSettings.py有关

## DATA/assets/ButtonName；PageName；PopupName类

皆为静态截图的命名类

## AllPage/Page类

初始构想是维护一个页面间的跳转图，这样当我们想要到达哪个游戏页面时，调用Page.to_page(PageName.PAGE_TARGET)即可。

后面取消了此类构想，将页面的跳转放到了每一个TASK里面，通过Page.is_page()判断当前页面是否是该页面

## AllTask/Task类

Task类的实例就是用户想要完成的自动化任务，每个任务都会有pre_condition, on_run, post_condition阶段。run方法定义了Task实例的运行逻辑。

其中pre_condition是此任务是否可以进行的判断，当pre_condition返回False时，将会跳过此任务。

on_run定义了任务具体的执行步骤，在on_run内部，使用self.run_until(func1, func2, times)来持续性地执行func1操作, 直到func2成立，或执行了times次，每次尝试执行后都会重新进行截图操作。使用match(page_pic(PageName.PAGE_TARGET))来进行图片匹配操作。使用click(button_pic(ButtonName.BUTTON_TARGET))点击图像匹配中心点，或使用click((224, 789))点击横轴224，纵轴789位置。

post_condition是任务的后置判断，主要判断此任务结束时的位置是否可控，是否跳转到了其他的页面。后面发现后置判断完全可以省略或放进on_run的最后，此方法可以废弃。

在modules/AllTask文件夹下的所有与子文件夹同名的Task，都应是一个每日任务之一，比如咖啡馆相关任务/商店购买任务，它们将会被放进myAllTask列表内进行解析运行。这些与子文件夹同名的每日任务Task默认都是从游戏主页，也就是live2D界面开始运行，运行结束时应当回到游戏主页。

## 添加一个新的任务的开发步骤

1. 使用test里的截图功能截取所需的图片pattern。将各个服务器下的截图放入各个assets文件夹内相应子文件夹内，并一致重命名。
2. 在DATA/assets/下的ButtonName.py或PageName.py或PopupName.py内用文件名注册此pattern。
3. 在modules/AllTask/下新建此任务的文件夹，并在其内部新建同名py文件，将ataskformat.py内的内容复制粘贴进去，修改类名与构造函数的name默认属性为你的task名字。在modules/AllTask/__init__内导入此任务类
4. 修改此新任务的py文件内容
5. 在modules/AllTask/myAllTask.py的task_dict里添加 用户配置项目文件内的任务名 与 此新任务的 实例间映射关系
6. 在gui/__init__的real_taskname_to_show_taskname里添加 用户配置项目文件内的任务名 与 gui里显示的文本间的对应关系
7. 在DATA/i18n里添加对应文本
8. 如要添加配置项，在modules/configs/defaultSettings.py里添加配置默认值以及映射函数，在modules/configs/settingMaps定义映射关系即可。
