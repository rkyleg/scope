# <img src="armadillo/img/armadillo.png" height="48px;"> Armadillo IDE
Armadillo is a lightweight, cross-platform IDE for Python, web development and more. Armadillo is coded in Python with PyQt for the UI and also some html5 interfaces via Qt's built-in WebKit browser (QWebView).

# Screenshots
![Alt text](extra/screenshot.png "Screenshot")

## Features
- Cross Platform - Linux, Windows, and Mac (not tested)
- Support for multiple languages (Python, Javascript, HTML, Markdown, more...)
- Mostly lightweight
- Code outline for code organization
- Easily create plugins with Python and PyQt
- Multiple options for code editors (Ace, Scintilla, CKEditor)
- Run code from IDE

## Installing
### Running with Python (source)
1. Install [Python](https://www.python.org/downloads/release/python-279/) (version 2.7 or 2.6 required)
2. Install [PyQt](http://www.riverbankcomputing.com/software/pyqt/download) (between versions 4.8-4.11 required)
2. Additional Linux requirements (installed by default with PyQt on Windows)
    - Python-Qsci (Required on Linux.  PyQt Windows default install includes this)
    - pyqt4-dev-tools (if you want to use pyqt converter on Linux)
    - Easiest way to install for Debian/Ubuntu in command Window:
        - \> su
        - \> apt-get install pyqt4-dev-tools python-qt4 python-qscintilla2 qt4-designer
3. Run armadillo/armadillo.py

### Windows Executable
1. [Download Windows zip](https://github.com/convolutedlogic/armadillo/archive/windows.zip)
2. Extract zip folder somewhere
3. Run windows/Armadillo.exe

### Development
The latest development version is available [here](https://github.com/convolutedlogic/armadillo/tree/dev)

## Documentation
- **[Overview](armadillo/doc/overview.md)** - Overview of main window features
- **[Editors](armadillo/doc/editors.md)** - multiple code editors are available
- **[Plugins](armadillo/doc/plugins.md)** - comes with default plugins
    - [Outline](doc/plugins_outline.md) - Outline plugin for code organization
    - Output - run your code in a separate process in the IDE.
    - [Python Shell](doc/plugins_pyconsole.md) - integrated Python Console
    - PyQt Converter - convert Qt ui files to PyQt .py files
    - Find / Replace - advanced find/replace tool
    - Snippets - store and retreive useful code snippets
- **[Settings](armadillo/doc/settings.md)** - settings are stored in config file
- **[License](LICENSE)** - GNU General Public License (GPL 3)
- **[Keyboard Shortcuts](armadillo/doc/keyboard_shortcuts.md)**
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
- [cx_Freeze](http://cx-freeze.sourceforge.net/) - for generating Windows and Linux binaries
- [File Icon Set](https://github.com/teambox/Free-file-icons) - for most file type icons
- [ConfigObj.py](http://www.voidspace.org.uk/python/configobj.html) - for settings file
- [CommonMark.py](https://github.com/rolandshoemaker/CommonMark-py) - utilized for [markdown](http://commonmark.org/)