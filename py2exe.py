"""
This file is used for the auto-py-to-exe package with the py2exe.json file and (hopefully) trick windowsdefender into thinking my program isn't a virus.
This part of code is suggested by the [1 METHOD](https://stackoverflow.com/a/64800999/19288094)
"""
from base64 import b64encode,b64decode
import sys,os
encoding = "utf-8"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(resource_path("Rename.py"),"r",encoding=encoding) as py:
    code = b64encode(bytes(py.read(),encoding))

exec(b64decode(code))