# Welcome to join the development

Welcome to improving this project. But kindly keep in mind that the idea of this project is to help sensei finish **"daily task"**, but not **"help them play the game or complete events"**. So it will be good to focus on those daily tasks which can be completed everyday.

All specs of functions will be translated into English soon.

It spent me just one afternoon to generate the structure of this project from 0, so there may be many problems in it. Good message is that we just need to keep the idea "**daily task**".

# Structure

The whole system is splitted into Page, Popup, Button and Task.

Page, Popup and Button do the identification of the situation.

Task will do the jobs of daily tasks.

## Page, Popup, Button

A Page is an Activity which means a big background change between two Pages (from MainPage to Cafe, etc), while Popup is the pop up windows in front of these Pages. Button is any clickable buttons (Confirm, Cancel, etc). 

All Page, Popup and Button has their own identity pattern, which is kept in `./assets` folders. Each of this pattern needs to be registered in `./assets/PageName.py`, `./assets/PopupName.py` and `./assets/ButtonName.py`.

So that we can get the url path of any pattern picture like `urlpath = button_pic(ButtonName.BUTTON_CANCEL)`, this also works for Page and Popup.

By using `match(urlpath)`, we try to match this pattern in the screenshot `./screenshot.png`.

So that is how we can get to know where we are.

## Task

Task is going to let us know what to do.

A Task contains three hooks(pre_condition(), on_run(), post_condition())

1. pre_condition(): defined whether the task is ready to perform, or whether it is needed to perform this task. For example, check the cafe power is not null before collect cafe power.

    if pre_condition() don't return True, then this task will be jumped over.

    Typically, all daily task(those tasks which have a folder name in `./AllTask`) starts from main page.

    Do not click or swipe in this hook.

2. on_run(): defines what to do when perform the task.

    In this hook, I highly recommend using `Task.run_until()` instead of calling `click()` and `match()`.

    `run_until(func1, func2, times = n)` will run func1 at most n times or until func2 once return True. It can help solve the delay of the page switching and the missing of one touch caused by network

    For example, if we want to keep pressing the cancel button until we come back to the timetable page. We can write just like:

    ```python
    def on_run(self):
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CANCEL)),
            lambda: match(page_pic(PageName.PAGE_TIMETABLE)),
            times = 3
        )
    ```

3. post_condition(): defines whether the task is successfully completed and stayed at which page.

    Typically, all daily task(those tasks which have a folder name in `./AllTask`) ends at the main page.

    Do not click or swipe in this hook. Clear all side effect of the task in `on_run()`