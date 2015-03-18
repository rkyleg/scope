# <img src="../img/armadillo.png" height="48px;"> About Armadillo IDE
Armadillo is a lightweight, cross-platform IDE for Python, web development and more. Armadillo is primarily coded in Python with PyQt for the main UI with some html5 interfaces via Qt's built-in WebKit browser (QWebView).

![](../../extra/screenshot.png)

## Design Goals
Armadillo hearkens back to the time of simple, light-weight IDEs that provide more than an editor, while also trying to stay out of the way of coding. The ui design is fairly minimalistic, while providing easy access to common tools. Keyboard shortcuts provide quick ways to show and hide plugins to get them out of the way when not needed.

Armadillo's current focus is on Python and web development due to the main developer's use, but Armadillo can be set up for use with many languages.

# Features
- Lightweight and simple interface
- **Multiple editors** to choose from (Scintilla, Ace, CKEditor). For example, you can use Scintilla for Python and Ace for JavaScript.
- **Plugins** - Armadillo comes with default plugins located to the left,  bottom and right of the editor. You can create your own plugins with Python and PyQt.
    - **File Browser** - view files for the current workspace
    - **Outline** - Provides an outline of objects and functions for some languages
    - **Python Shell** - an interactive Python shell
    - **Snippets** - create and manage snippets of code you may want to reuse
    - **Preview** - HTML and Markdown preview (Webkit Webbrowser)
- **Run code** - run code from the IDE and see any output through the Output plugin. Depending on the language, you may need to install additional tools.
- **Screen Shortcuts** - Multiple quick keys to show/hide plugins to make the best use of screenspace and get plugins out of the way.
- **Workspaces** - Armadillo will keep track of open files and the file browser path for multiple workspaces.
- Customize with a settings file.
- **HUD** (F1) - heads up display for viewing current open files and more.
- Keyboard shortcuts to show and hide plugins to make the most of your screenspace

## Modify
Since Armadillo is open source, it can easily be forked and modified. I created Armadillo so I could have full customization of an IDE. You can modify Armadillo for your own customization. You can create your own plugins and add other editors like CodeMirror. Use the existing editors and plugins as templates for your own.

## Future
There are many features to add to an IDE. Features will only be added as long as they keep with the lightweight theme - or will be optional. While usable, the version 1.x series is still an ongoing design iteration. The 2.x version will likely change some of the editor and plugin API, assigned keyboard shortcuts, and settings layout.

Because Armadillo is hackable, there may be a plethora of plugins. A plugin manager is planned for the 2.0 release or sooner.

## License
Armadillo is licensed under the GPL3

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
    
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
    
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        
[LICENSE](../../LICENSE.txt)