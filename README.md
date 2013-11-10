![Alt text](/img/afide.png "afide") afide
=====
another freakin IDE

Pronounced as aphid

**Warning** - This is still in the early stages of development.  Use at your own risk.

![Alt text](/img/screenshot.png "Screenshot")

About
==
I didn't really want to create a new IDE, but I wanted total customization while keeping it lightweight.  afide is inspired by SPE, Geany, Notepad++ and Spyder.  afide is written in Python with PyQt (and sometiems HTML5) for the UI.  HTML5 is utilized with Qt's built in WebKit (WebView).

The goals of afide:
- Cross Platform (Linux, Windows, and maybe Mac)
- Handle Multiple languages (Python, Javascript, HTML,...)
- Easily create plugins with Python and PyQt
- Mostly Lightweight
- Be able to utilize existing code editors (Scintilla, CKEditor, Ace, Scintilla)
- Customizable and easily extensible

Requirements
==
afide is not yet compiled so you must run it with Python.  I have only tested it on Linux (Mint 15) and Windows 7 so far.
- Python 2.6-2.7 (Not tested with 2.6 although 2.6 should work)
- PyQt 4.8-4.9 (Not tested with 5.x - probably doesn't work)
- Python-Qsci
- pyqt4-dev-tools (if you want to use pyqt converter on linux)

Settings
==
Settings are stored in settings.py

Current State (as of October 2013)
==
- Cross Platform (Windows and Linux)
- Multiple language support (although somewhat limited)
- Some settings saved and Workspaces available
- Scintilla is the main editor available
- Can run Python files and html (in browser)
- Python Shell plugin somewhat buggy
- Outline plugin works for Python, CSS, HTML, and JavaScript

Future State
==
- User preferences interface
- Check if open files changed outside of editor
- Some kind of integrated help - for online resources
- Save user settings separate from default settings
- Better code completion support