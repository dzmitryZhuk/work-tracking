from utils import install_python_module
### install module PySimpleGUI for showing window then
install_python_module('PySimpleGUI')
#############################################################################################

PROGRAM_NAMES = []
STRING_ADD = 'Add'
STRING_REMOVE = 'Remove'
STRING_CANSEL = 'Cansel'
STRING_KILL = 'Stop tracking'
STRING_TITLE = 'Work tracking'
STRING_NEXT = 'Next'
STRING_INPUT = 'Input'
MODULES_NAMES = ['swinlnk', 'psutil']
CFG_FILE = 'main.cfg'

import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')
### layout for install modules
progressbar = sg.ProgressBar(len(MODULES_NAMES), orientation='h', size=(51, 10), key='progressbar')
layout = [ [sg.Push(), sg.Text('Installing modules'), sg.Push()],
                    [sg.Push(), progressbar, sg.Push()],
                    [sg.Button(STRING_CANSEL), sg.Button(STRING_NEXT, disabled=True)]
                    ]
###

window = sg.Window(STRING_TITLE, layout, finalize=True)
for i, name in enumerate(MODULES_NAMES):
    window.read(timeout=0)
    if not install_python_module(name):
        exit(1)
    progressbar.update(i + 1)
window[STRING_NEXT].update(disabled=False)
while True:
    event, values = window.read()
    if event == STRING_CANSEL:
        window.close()
        exit(0)
    if event == STRING_NEXT:
        break

window.hide()    
window.close()
#############################################################################################

### main layout
button_add = sg.Button(STRING_ADD,
                        tooltip=f'Enter name of the target program and click on this button to {STRING_ADD.lower()} the program')
button_remove = sg.Button(STRING_REMOVE, disabled=True,
                            tooltip=f'Select the name of the program and click on this button to {STRING_REMOVE.lower()} the program')
button_kill = sg.Button(STRING_KILL,
                        tooltip=f'Stops script that tracking programs')
block_list = sg.Listbox(PROGRAM_NAMES, enable_events=True, expand_x=True, expand_y=True)
block_input = sg.Input(enable_events=True, key=STRING_INPUT)
layout = [  [sg.Push(), sg.Text('Tracking programs names'), sg.Push()],
            [block_list],
            [sg.Text('Enter target program name or path to .exe file'), block_input],
            [button_add, button_remove, sg.Push(), button_kill] ]
###
window = sg.Window(STRING_TITLE, layout, resizable=True, finalize=True)
block_input.bind("<Return>", "_Enter")

#############################################################################################
from utils import stop_python_script
from utils import cfg_read_names
from utils import cfg_write_names

PROGRAM_NAMES = cfg_read_names(CFG_FILE)
block_list.update(PROGRAM_NAMES)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == STRING_ADD:
        if len(block_input.get()):
            PROGRAM_NAMES.append(block_input.get())
            block_input.update('')
            cfg_write_names(CFG_FILE, PROGRAM_NAMES)
            block_list.update(PROGRAM_NAMES)

    if event == STRING_REMOVE:
        for el in block_list.get():
            PROGRAM_NAMES.remove(el)
        cfg_write_names(CFG_FILE, PROGRAM_NAMES)
        block_list.update(PROGRAM_NAMES)

    if event == STRING_KILL:
        stop_python_script('tracking.pyw')

    if len(block_list.get()):
        button_remove.update(disabled=False)
    else:
        button_remove.update(disabled=True)

    if event == STRING_INPUT + '_Enter':
        if len(block_input.get()):
            PROGRAM_NAMES.append(block_input.get())
            block_input.update('')
            block_list.update(PROGRAM_NAMES)
            cfg_write_names(CFG_FILE, PROGRAM_NAMES)

window.close()   