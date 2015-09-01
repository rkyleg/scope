_**WARNING: Scope is currently in alpha stage and is likely not suitable for daily use.**_

*Scope is a redesign of Armadillo IDE*

# <img src="style/img/scope.png" height="48px;"> Scope IDE
Scope is a lightweight, cross-platform IDE for Python, web development and more. Scope is primarily coded in Python with PyQt for the main UI with some html5 interfaces via Qt's built-in WebKit browser (QWebView).

# Screenshots
<a href="extra/scope_home.png" target="_blank" title="Scope Home Screen"><img src="extra/scope_home.png" height=200></a>
<a href="extra/scope_editor.png" target="_blank" title="Scope Screenshot"><img src="extra/scope_editor.png" height=200></a>
<a href="extra/scope_tabs.png" target="_blank" title="Scope File Tabs"><img src="extra/scope_tabs.png" height=200></a>

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
2. Additional Linux requirements (installed by default with PyQt on Windows)
    - Python-Qsci (Required on Linux.  PyQt Windows default install includes this)
    - pyqt4-dev-tools (if you want to use pyqt converter on Linux)
    - Easiest way to install for Debian/Ubuntu in command Window:
        - \> sudo apt-get install pyqt4-dev-tools python-qt4 python-qscintilla2 qt4-designer
3. Run Scope.py

### Installing on Mac OSX
1. Requirements: Python, qt, sip, pyqt, qscintilla2
	-These can all be installed with homebrew

### Development
The latest development version is available [here](https://github.com/lucidlylogicole/scope/tree/dev)

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
- [ConfigObj.py](http://www.voidspace.org.uk/python/configobj.html) - for settings file
- [CommonMark.py](https://github.com/rolandshoemaker/CommonMark-py) - utilized for [markdown](http://commonmark.org/)