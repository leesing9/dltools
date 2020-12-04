import os
import stat

osName = os.name

def consolClear():
    if osName == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)