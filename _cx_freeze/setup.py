import sys
from cx_Freeze import setup, Executable

# Command:
# python setup.py build

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "os",
        'json',
        'PyQt4.QtCore',
        'PyQt4.QtGui',
        'PyQt4.QtWebKit',
        'PyQt4.QtNetwork',
        'PyQt4.Qsci',
        'code',
        'importlib',
##        'markdown',
        'shutil',
        'webbrowser',
        'threading',
        ], 
    "excludes": ["tkinter",'numpy','scipy'],
    'icon':'../style/img/scope.ico',
    'copy_dependent_files':1,
    'bin_includes':['../scope/scope.py'],
    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Scope",
        version = "0.3",
        description = "IDE",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Scope.py", base=base)])