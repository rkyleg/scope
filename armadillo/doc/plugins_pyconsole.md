<link rel="stylesheet" type="text/css" href="doc.css">

# [Home](start.html) | [Plugins](plugins.md) | Python Shell (py_console)

The Armadillo Python Shell, PyConsole, is a modified version of [pycute4](http://pyqtlive.googlecode.com/hg/pycute4.py) by Rob Reilink.  pycute4 derives from PyCute3.py by Gerard Vermeulen [http://gerard.vermeulen.free.fr/]() and was ported for Qt4.

# Notes
- Unless you are running from Python source, the shell uses Python 2.7
- If you don't have Python 2.7 installed and are using the Windows binary, then you will have limited Python functions - only what is bundled with Armadillo.
- Ctrl +L - will launch the shell outside of Armadillo with your default Python install (Python and PyQt must be installed).
- You can access Aramdillo from the shell with the *armadillo* object.  **Be careful as you can lose work**.

        armadillo.currentWidget() # Gets the current editor widget
        armadillo.currentWidget().getText() # Gets the text from the current editor widget
        