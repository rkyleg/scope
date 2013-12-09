Armadillo IDE
![Alt text](img/armadillo.png "afide")
=====

**Warning** - This is still in the early stages of development.  Use at your own risk.

![Alt text](extra/screenshot.png "Screenshot")

About
==
I didn't really want to create a new IDE, but I wanted total customization while keeping it lightweight.  afide is inspired by SPE, Geany, Notepad++ and Spyder.  afide is written in Python with PyQt (and sometiems HTML5) for the UI.  HTML5 is utilized with Qt's built in WebKit (WebView).

The goals of afide:
- Cross Platform (Linux, Windows, and maybe Mac)
- Handle Multiple languages (Python, Javascript, HTML,...)
- Easily create plugins with Python and PyQt
- Mostly Lightweight
- Be able to utilize existing code editors (Scintilla, CKEditor, Ace, more...)

Requirements
==
afide is not yet compiled so you must run it with Python.  I have only tested it on Linux (Mint 15) and Windows 7 so far.
- Python 2.6-2.7 (Not tested with 2.6 although 2.6 should work)
- PyQt 4.8-4.9 (Not tested with 5.x - probably doesn't work)
- Python-Qsci
- pyqt4-dev-tools (if you want to use pyqt converter on linux)

Settings
==
- Settings are stored in settings.py
- *settings structure still in a state of change*

To Do and Roadmap
==
- **[Roadmap](extra/roadmap.md)** - The current state of Afide and future plans
- **[Todo](extra/todo.md)** - List of to do and status

Reference
==
Thanks to the following tools that Afide is built on:

- [Python](http://python.org) 
- [PyQt](http://www.riverbankcomputing.com/software/pyqt) - UI
- [Scintilla](http://www.scintilla.org/)/QsciScintilla (via [PyQt](http://www.riverbankcomputing.com/software/pyqt))
- [Ace Editor](http://ace.c9.io/) - HTML5 based code editor
- [CKEditor](http://ckeditor.com/) - rich text html WYSIWIG editor
- [Silk Icons](http://www.famfamfam.com/lab/icons/silk/) - main ui icon set
- [Python Markdown2](https://github.com/trentm/python-markdown2) - for generating html from markdown
- [File Icon Set](https://github.com/teambox/Free-file-icons) - for most file type icons