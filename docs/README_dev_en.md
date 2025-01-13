# Project Structure

```
- BAAH_CONFIGS/ User-configured tasks to be executed
- DATA/ Various static resources required for this project and multilingual support
- docs/ Documentation
- gui/ User interface related to configuration
  |-components/ Reusable components
  |-pages/ Pages and subpages
  |-__init__.py Editing pages for a config
- modules/ Main modules
  |- AllPage/ Defines the Page class, typically related to page-level navigation
  |- AllTask/ Defines the Task class, typically related to daily tasks
  |- configs/ Defines the MyConfigger class, related to various config operations required for this project
  |- utils/ Defines utility classes related to adb and image operations
- tools/ Static resources for called adb and libraries; note that these resources are not in GitHub
  |- adb/
  |- nicegui/
  |- pponnxcr/
- BAAH.py Executes tasks specified by a user configuration file
- jsoneditor.py Entry point for the GUI
- main.py Entry point for the main program
- requirements.txt All dependencies
```

# Project Execution

The automatic script project runs from main.py as the entry point. It reads the user-specified configuration file from the command line and then parses the daily tasks for this user configuration file through the myAllTask class under AllTask. It creates corresponding Task instances for each task in a list and sequentially runs these Task instances in BAAH.py.

# Project Package

Mainly use pyinstaller for packaging. The packaging command is

```python
python package.py
```

# Key Classes

## modules/configs/Configger Class

Located in modules/configs/, MyConfig controls the contents of the user configuration file. Its key behaviors are assigning default values to user configuration files that have not appeared and deducing unknown configurations through known configurations. These two functions are related to settingMaps.py and defaultSettings.py, respectively.

## DATA/assets/ButtonName; PageName; PopupName Classes

These are naming classes for static screenshots.

## AllPage/Page Class

The initial idea was to maintain a diagram of page transitions so that when we want to reach a particular game page, we can call Page.to_page(PageName.PAGE_TARGET).

Later, this idea was abandoned, and page transitions were moved into each TASK. Page.is_page() is used to determine if the current page is the desired page.

## AllTask/Task Class

An instance of the Task class is an automation task that the user wants to complete. Each task has pre_condition, on_run, and post_condition phases. The run method defines the logic for running Task instances.

The pre_condition is the judgment of whether this task can proceed. When pre_condition returns False, the task will be skipped.

on_run defines the specific execution steps of the task. Inside on_run, use self.run_until(func1, func2, times) to continuously execute func1 operation until func2 is established or it has been executed times times. Screenshot operations are performed using match(page_pic(PageName.PAGE_TARGET)). Clicking on image matches the center point using click(button_pic(ButtonName.BUTTON_TARGET)) or click((224, 789)) to click at the coordinates (224, 789) on the screen.

post_condition is the post-judgment of the task, mainly to determine if the task is in a controllable state when it ends, and if it has transitioned to other pages. Later, it was found that the post-condition judgment can be completely omitted or placed at the end of on_run; this method can be deprecated.

All the Task folders in the modules/AllTask directory with the same name as the subfolders should be one of the daily tasks, such as tasks related to the café or shop purchases. They will be placed in the myAllTask list for parsing and execution. These daily Task instances with the same name as the subfolders should all start running from the game's main page, which is the live2D interface, and should return to the game's main page when the execution is complete.

## Steps to Add a New Task

1. Use the screenshot feature in the test to capture the required image pattern. Place screenshots from different servers into the respective subfolders of the assets folder and rename them consistently.
2. Register this pattern in ButtonName.py, PageName.py, or PopupName.py under DATA/assets using the file name.
3. Create a new folder for this task in modules/AllTask/ and create a same-named .py file inside it. Copy and paste the contents of ataskformat.py into it, and modify the class name and the default attribute of the constructor's name to your task name. Import this task class in modules/AllTask/__init__.
4. Modify the content of this new task's .py file.
5. Locate the `TaskName` in modules/AllTask/myAllTask.py, add a task name that will be stored in the config. And add corresponding `i18n_key_name` and `task_module` in `TaskInstanceMap` of this `task_config_name`
6. In real_taskname_to_show_taskname in gui/__init__, add a correspondence between the task name in the user configuration file and the text displayed in the GUI.
7. Add corresponding text in DATA/i18n.
