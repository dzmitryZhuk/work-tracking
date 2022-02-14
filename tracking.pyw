from swinlnk.swinlnk import SWinLnk
import os
import time
import datetime
import win32gui

START = "start>"
STOP = "stop>"
PROGRAMS = ["AnyDesk"]
DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\data\\"

# add to startup
def startup():
    user_path = os.path.expanduser('~') # path to user directory
    path_link = f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{os.path.basename(__file__)}" + ".lnk"
    if not os.path.exists(path_link):
        swl = SWinLnk()
        swl.create_lnk(os.path.realpath(__file__), path_link)
        print("Added to startup")

# create directory where will be all info aboat working time
def dir():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
        print("folder for data created")
    if len(PROGRAMS) > 0:
        for name in PROGRAMS:
            subdir(name)

# create subdirectory for program
def subdir(name):
    if not os.path.exists(DIRECTORY + '\\' + name + '\\'):
        os.makedirs(DIRECTORY + '\\' + name + '\\')
        print("\'" + name + "\' folder created")

#########################################################################################

was_started = {}
for prog in PROGRAMS:
    was_started[prog] = False
current_day = datetime.datetime.now().date().strftime("%d")

startup()
while True:
    dir()
    now = datetime.datetime.now()
    if len(PROGRAMS) > 0:
        # if u are still working but it's a new day
        temp_day = now.date().strftime("%d")
        if temp_day != current_day:
            previous_day = current_day
            current_day = temp_day
            for program_name in PROGRAMS:
                if was_started[program_name] == True:
                    file = open(DIRECTORY + '\\' + program_name + '\\' + now.date().strftime("%Y_%m_") + previous_day, 'a')
                    file.write(STOP + " " + "23:59:59" + '\n')
                    file.close()

                    file = open(DIRECTORY + '\\' + program_name + '\\' + now.date().strftime("%Y_%m_") + current_day, 'a')
                    file.write(START + " " + now.time().strftime("%H:%M:%S") + '\n')
                    file.close()

        # check if programm is running
        process_running = {}
        for prog in PROGRAMS:
            process_running[prog] = False
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                name = win32gui.GetWindowText( hwnd )
                for program_name in PROGRAMS:
                    if program_name.lower() in name.lower():
                        process_running[program_name] = True
        win32gui.EnumWindows( winEnumHandler, None )
        
        # start working
        for program_name in PROGRAMS:
            if process_running[program_name] == True and was_started[program_name] == False:
                was_started[program_name] = True
                file = open(DIRECTORY + '\\' + program_name + '\\' + now.date().strftime("%Y_%m_") + current_day, 'a')
                file.write(START + " " + now.time().strftime("%H:%M:%S") + '\n')
                file.close()

        # stop working
        for program_name in PROGRAMS:
            if process_running[program_name] == False and was_started[program_name] == True:
                was_started[program_name] = False
                file = open(DIRECTORY + '\\' + program_name + '\\' + now.date().strftime("%Y_%m_") + current_day, 'a')
                file.write(STOP + " " + now.time().strftime("%H:%M:%S") + '\n')
                file.close()    

    time.sleep(1)
