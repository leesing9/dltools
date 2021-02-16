import os
import stat
import json

from collections import defaultdict
from pathlib import Path

osName = os.name

def consolClear():
    if osName == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def readJson(path:Path)->defaultdict:
    with open(path,'r') as f:
        cfg = defaultdict(str,json.load(f))
    return cfg

def saveJson(path:Path, jsonDict:defaultdict)->None:
    with open(path, 'w') as f:
        json.dump(jsonDict, f,ensure_ascii=False, indent=4)
