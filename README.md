_**Scope is currently in beta stage.** For more information on where this is going, please see the [roadmap](/docs/roadmap.md)_

# <img src="style/img/scope.png" height="48px;"> Scope IDE
Scope is a lightweight, cross-platform IDE for Python, web development and more. Scope is primarily coded in Python with PyQt for the main UI with some html5 interfaces via Qt's built-in WebKit browser (QWebView).

## Screenshots
<a href="docs/img/scope_home.png" target="_blank" title="Scope Home Screen"><img src="docs/img/scope_home.png" height=250></a>
<a href="docs/img/scope_editor.png" target="_blank" title="Scope Screenshot"><img src="docs/img/scope_editor.png" height=250></a>
<a href="docs/img/scope_tabs.png" target="_blank" title="Scope File Tabs"><img src="docs/img/scope_tabs.png" height=250></a>

## Features
- Cross Platform - Linux, Windows, and Mac (not tested)
- Support for multiple languages (Python, Javascript, HTML, Markdown, more...)
- Focus on lightweight
- Outline for code organization
- Multiple options for code editors (Ace, Scintilla, CKEditor)
- Run code from IDE with output screen
- Splitview preview for html and markdown
- Extend with your own plugins created with Python and PyQt
- Multiple workspaces can be open at once
- New interface for selecting tabs/open files

## Installing

### Running with Python (source)
1. Install [Python](https://www.python.org/downloads/release/python-279/) (version 2.7 or 2.6 required)
2. Install [PyQt](http://www.riverbankcomputing.com/software/pyqt/download) (between versions 4.8-4.11 required)
3. Additional Linux requirements (installed by default with PyQt on Windows)
    - Python-Qsci (Required on Linux.  PyQt Windows default install includes this)
    - pyqt4-dev-tools (if you want to use pyqt converter on Linux)
    - Easiest way to install for Debian/Ubuntu in command Window:
        - \> sudo apt-get install pyqt4-dev-tools python-qt4 python-qscintilla2 qt4-designer
4. Download and extract [Scope.zip](https://github.com/lucidlylogicole/scope/archive/master.zip) *(or clone with git)*
5. Run Scope.py

### Windows Executable

1. Download [Windows zip](https://github.com/lucidlylogicole/scope/archive/windows.zip)
2. Extract zip folder to desired location
3. Run *windows/Scope.exe*

### Development
The latest development version is available [here](https://github.com/lucidlylogicole/scope/tree/dev)

## Documentation
- **[Overview](docs/overview.md)**
- **[Opening a File](docs/open_file.md)**
- **[Keyboard Shortcuts](docs/keyboard_shortcuts.md)**
- **[Editors](docs/editors.md)**
- **[Roadmap](docs/roadmap.md)**

## License
- **[License](LICENSE.txt)** - GNU General Public License (GPL 3)

## Reference
Thanks to the following tools that Scope is built on:

- [Python](http://python.org) 
- [PyQt](http://www.riverbankcomputing.com/software/pyqt) - UI
- [Scintilla](http://www.scintilla.org/)/QsciScintilla (via [PyQt](http://www.riverbankcomputing.com/software/pyqt))
- [Ace Editor](http://ace.c9.io/) - HTML5 based code editor
- [CKEditor](http://ckeditor.com/) - rich text html WYSIWIG editor
- [Silk Icons](http://www.famfamfam.com/lab/icons/silk/) - main ui icon set
- [cx_Freeze](http://cx-freeze.sourceforge.net/) - for generating Windows and Linux binaries
- [File Icon Set](https://github.com/teambox/Free-file-icons) - for most file type icons
- [CommonMark.py](https://github.com/rolandshoemaker/CommonMark-py) - utilized for [markdown](http://commonmark.org/)