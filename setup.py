from cx_Freeze import setup, Executable
import sys, os

os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Python36-32\tcl\tk8.6'


base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("game.py", base=base)]

packages = ["idna", "os", "random", "tkinter"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "eMZak",
    options = options,
    version = "0.9",
    description = 'moja prva hra',
    executables = executables
)