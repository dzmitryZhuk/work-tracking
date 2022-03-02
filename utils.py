import psutil
import os
import re
import configparser

SPLITTER_FOR_CFG = '|'

def stop_python_script(name=None):
    if name is not None:
        for p in psutil.process_iter():
            if 'python' in p.name() and '.exe' in p.name():
                for cmd_param in p.cmdline():
                    l = re.split(r'[\\\/]', cmd_param)
                    base_name = l[len(l) - 1]
                    if os.path.basename(name) == base_name:
                        p.kill()

def install_python_module(module=None):
    if module is not None:
        return_code = os.system(f'pip install {module}')
        return return_code == 0
    return False    

def is_python_script_running(name=None):
    if name is not None:
        for p in psutil.process_iter():
            if 'python' in p.name() and '.exe' in p.name():
                for cmd_param in p.cmdline():
                    l = re.split(r'[\\\/]', cmd_param)
                    base_name = l[len(l) - 1]
                    if os.path.basename(name) == base_name:
                        return True
    return False

def strToNames(str):
    return re.split(fr'[{SPLITTER_FOR_CFG}]', str)

def strFromNames(names):
    str = ''
    for i, name in enumerate(names):
        str = str + name
        if i < len(names) - 1:
            str = str + SPLITTER_FOR_CFG
    return str

def cfg_read_names(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    names = config.get("Main", "names")
    return strToNames(names)

def cfg_write_names(file_path, names):
    config = configparser.ConfigParser()
    config.add_section("Main")
    config.set("Main", "names", strFromNames(names))

    with open(file_path, "w") as config_file:
        config.write(config_file)
