# Folder for tests
____
It was decided to optimize the script and reduce the time spent searching for all currently running programs. The following solution was found: using the `win32gui` module instead of `pywinauto`, because [test](test_time_windowTitleModules.py) showed that the new solution works ~60 times faster than the previous one: 
[picture](test_time_windowTitleModules.png)
