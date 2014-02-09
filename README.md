# Armadillo IDE
![Alt text](extra/screenshot.png "Screenshot")

## About
Armadillo is a lightweight,cross-platform IDE primarily for Python and Web Development, while also providing an editor for most languages.  Armadillo is inspired by SPE, Geany, Notepad++ and Spyder.  Armadillo is written in Python with PyQt and HTML5 for the UI.  HTML5 is utilized with Qt's built in WebKit (QWebView).

## Features:

- Cross Platform (Linux, Windows, and maybe Mac)
- Handle Multiple languages (Python, Javascript, HTML,...)
- Mostly Lightweight
- Code outline for code organization
- Easily create plugins with Python and PyQt
- Multiple options for code editors (Scintilla, CKEditor, Ace, more...)

## Requirements
Armadillo must be run with Python.  I have only tested it on Linux (Mint 15/16) and Windows 7 so far.
- Python 2.6-2.7 (Not tested with 2.6 although 2.6 should work)
- PyQt 4.8-4.10 (Not tested with 5.x - probably doesn't work)
- Python-Qsci (Required on Linux.  PyQt Windows installer has option to install this)
- pyqt4-dev-tools (if you want to use pyqt converter on Linux)

## Installing/Launching
1. Install prerequisites above (Python and PyQt)
2. Linux - Set armadillo.sh properties to execute and run.
4. Windows - Run armadillo.py

## Settings
- Settings are stored in [settings.py](settings.py)
- *settings structure still in a state of change*

## More Stuff
- **[License](LICENSE)** - GNU General Public License (GPL 3)
- **[Keyboard Shortcuts](doc/keyboard_shortcuts.html)**
- **[Roadmap](extra/roadmap.md)** - The current state of Armadillo and future plans
- **[Todo](extra/todo.md)** - List of to do and status

## Reference
Thanks to the following tools that Armadillo is built on:

- [Python](http://python.org) 
- [PyQt](http://www.riverbankcomputing.com/software/pyqt) - UI
- [Scintilla](http://www.scintilla.org/)/QsciScintilla (via [PyQt](http://www.riverbankcomputing.com/software/pyqt))
- [Ace Editor](http://ace.c9.io/) - HTML5 based code editor
- [CKEditor](http://ckeditor.com/) - rich text html WYSIWIG editor
- [Silk Icons](http://www.famfamfam.com/lab/icons/silk/) - main ui icon set
- [Python Markdown2](https://github.com/trentm/python-markdown2) - for generating html from markdown
- [File Icon Set](https://github.com/teambox/Free-file-icons) - for most file type icons