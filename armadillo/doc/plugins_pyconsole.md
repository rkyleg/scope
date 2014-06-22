<link rel="stylesheet" type="text/css" href="doc.css">

# [Home](start.html) | [Plugins](plugins.md) | Python Shell (py_console)

The Armadillo Python Shell, PyConsole, is a modified version of [pycute4](http://pyqtlive.googlecode.com/hg/pycute4.py) by Rob Reilink.  pycute4 derives from PyCute3.py by gerard vermeulen [http://gerard.vermeulen.free.fr/]() and was ported for Qt4.

# Notes
- Unless you are running from Python source, the shell uses Python 2.7
- The Python shell tries to add your Python 2.7 system path if installed.
- If you don't have Python 2.7 installed and are using the Windows binary, then you will have limited Python functions - only what is bundled with Armadillo.
- You can access Aramdillo from the shell with the *armadillo* object.  **Be careful as you can lose work**.

        armadillo.currentWidget() # Gets the current editor widget
