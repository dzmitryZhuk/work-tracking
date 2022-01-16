from pywinauto import Desktop
import os
import time
import datetime

START = "start>"
STOP = "stop>"
DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\data\\"
TARGET_PROGRAM_NAME = "AnyDesk"

# make directory where will be all info aboat working time
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
    print("Added to startup")

was_started = False
current_day = datetime.datetime.now().date().strftime("%d")

while True:
    now = datetime.datetime.now()

    # if u are still working but it's a new day
    if now.date().strftime("%d") != current_day and was_started == True:
        file = open(DIRECTORY + now.date().strftime("%Y_%m_") + current_day, 'a')
        file.write(STOP + " " + now.time().strftime("%H:%M:%S") + '\n')
        file.close()
        
        current_day = now().date().strftime("%d")

        file = open(DIRECTORY + now.date().strftime("%Y_%m_") + current_day, 'a')
        file.write(START + " " + now.time().strftime("%H:%M:%S") + '\n')
        file.close()

    # check if programm is running
    process_running = False
    windows = Desktop(backend="uia").windows()
    for w in windows:
        name = w.window_text()
        if TARGET_PROGRAM_NAME.lower() in name.lower():
            process_running = True
    
    # start working
    if process_running == True and was_started == False:
        was_started = True
        file = open(DIRECTORY + now.date().strftime("%Y_%m_%d"), 'a')
        file.write(START + " " + now.time().strftime("%H:%M:%S") + '\n')
        file.close()

    # stop working
    if process_running == False and was_started == True:
        was_started = False
        file = open(DIRECTORY + now.date().strftime("%Y_%m_%d"), 'a')
        file.write(STOP + " " + now.time().strftime("%H:%M:%S") + '\n')
        file.close()    

    time.sleep(1)
