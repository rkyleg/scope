_**WARNING: This development version of Armadillo is not suitable for use**_

*This version is in the middle of a redesign without tabs and is buggy.*

# <img src="armadillo/img/armadillo.png" height="48px;"> Armadillo IDE
Armadillo is a lightweight, cross-platform IDE for Python, web development and more. Armadillo is primarily coded in Python with PyQt for the main UI with some html5 interfaces via Qt's built-in WebKit browser (QWebView).

# Screenshots
<a href="extra/screenshot_home.png" target="_blank" title="Home/Startup Screen"><img src="extra/screenshot_home.png" height=200></a>
<a href="extra/screenshot.png" target="_blank" title="Editor with Outline"><img src="extra/screenshot.png" height=200></a>
<a href="extra/screenshotpreview.png" target="_blank" title="Markdown with preview"><img src="extra/screenshot_preview.png" height=200></a>
<a href="extra/screenshot_output.png" target="_blank" title="Running a file"><img src="extra/screenshot_output.png" height=200></a>
<a href="extra/screenshot_full_editor_mode.png" target="_blank" title="Full Editor Mode"><img src="extra/screenshot_full_editor_mode.png" height=200></a>
<a href="extra/screenshot_hud.png" target="_blank" title="Heads-up-display (HUD) F1"><img src="extra/screenshot_hud.png" height=200></a>

## Features
- Cross Platform - Linux, Windows, and Mac (not tested)
- Support for multiple languages (Python, Javascript, HTML, Markdown, more...)
- Focus on lightweight
- Outline for code organization
- Multiple options for code editors (Ace, Scintilla, CKEditor)
- Run code from IDE with output screen
- Splitview preview for html and markdown
- Extend with your own plugins created with Python and PyQt
- Head-up-display for selecting open files (F1)

## Installing
### Windows Executable
1. [Download Windows zip](https://github.com/convolutedlogic/armadillo/archive/windows.zip)
2. Extract zip folder somewhere
3. Run windows/Armadillo.exe

### Linux and Mac 
See next section (Running with Python)

### Running with Python (source)
1. Install [Python](https://www.python.org/downloads/release/python-279/) (version 2.7 or 2.6 required)
2. Install [PyQt](http://www.riverbankcomputing.com/software/pyqt/download) (between versions 4.8-4.11 required)
2. Additional Linux requirements (installed by default with PyQt on Windows)
    - Python-Qsci (Required on Linux.  PyQt Windows default install includes this)
    - pyqt4-dev-tools (if you want to use pyqt converter on Linux)
    - Easiest way to install for Debian/Ubuntu in command Window:
        - \> sudo apt-get install pyqt4-dev-tools python-qt4 python-qscintilla2 qt4-designer
3. Run armadillo/armadillo.py

### Development
The latest development version is available [here](https://github.com/convolutedlogic/armadillo/tree/dev)

## License
- **[License](LICENSE.txt)** - GNU General Public License (GPL 3)

## Documentation
- **[About](armadillo/doc/about.md)** - About Armadillo
- **[UI Overview](armadillo/doc/overview.md)** - Overview of main window features
- **[Editors](armadillo/doc/editors.md)** - multiple code editors are available
- **[Plugins](armadillo/doc/plugins.md)** - comes with default plugins
    - [Outline](armadillo/doc/plugins_outline.md) - Outline plugin for code organization
    - [File Browser](armadillo/doc/plugins_filebrowser.md) - View and open files in the folder of the workspace
    - [Output](armadillo/doc/plugins_output.md) - run your code in a separate process in the IDE.
    - [Python Shell](armadillo/doc/plugins_pyconsole.md) - integrated Python Console
    - PyQt Converter - convert Qt ui files to PyQt .py files
    - Find / Replace - advanced find/replace tool
    - Snippets - store and retrieve useful code snippets
- **[Settings](armadillo/doc/settings.md)** - settings are stored in config file
- **[Keyboard Shortcuts](armadillo/doc/keyboard_shortcuts.md)**

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