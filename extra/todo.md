# TODO

- [x] Move HUD to plugin (and keyboard shortcut)
- [] Move styles to stylesheet
- [] Move start page ? or at least formatting
- [x] handle plugins that aren't windows??
- [x] move plugin settings
- [x] use button classes for styling
- [x] update outline on load
- [] spellcheck plugin launches and can go off of selection or whole document
- [x] toolbar button - use class
- [x] fix outline not highlighting on open (at least for ace)

---
## Bugs
### Main

### Editors

### Plugins
- [_] Outline - fix tracking/updating (not quite right)
- [x] Filebrowser - show all files does not refresh in root

---
## Testing
- [_] Test with no plugins
- [_] with language that doesn't exist

---
## Armadillo 1.6
### Main
- [_] Install script to create shortcut
- [x] Python3 compatible imports (not full Python3 compatibility - yet)
- [x] Add middle click to close tab
- [x] Edit Workspace

### Editors
- [x] Add insertText function
- [x] Add color picker
- [_] Improve Ace right click menu layout and available functions

### Plugins
- [_] Plugin menu for extra, not default open plugins
- [x] Filebrowser - add refresh menu
- [x] Snippets - change copy to insert
- [_] Preview - option to utilize github markdown generation

---
## Armadillo 1.7
- [_] Plugins manager for importing plugins
- [_] store activePlugin settings separate from other settings - handled by Armadillo and not user editable
- [_] Github markdown option
- [_] markdown preview - image max width

---
## Armadillo 2.0
### Main
- [_] Add more language icons
- [_] Continuously check for file changes and alert
- [_] Themes
- [_] Auto or manual easy updates of Armadillo
- [_] Redo keyboard shortcuts F1-F12 to fit with overall strategy?
- [_] Customizable toolbar - users can add their own tools/shortcuts

### Editors

### Plugins
- [_] Plugin manager
- [_] Auto or manual easy updates of plugins

---
## Misc updates
Unplanned updates for any version and may or may not happen.

### Main
- [_] Add header comment button (use outline protocol)
- [_] load widgets other than files
- [_] hide statusbar text after a given time
- [_] save splitter states
- [_] Linux, Mac binaries
- [_] pip package
- [_] right click main menu
- [_] Python3 compatible
- [_] FileHUD - tab, shift+tab to move between tabs
- [_] FileHUD - hovering or current changed (before keyup) will change tab

### Editors
- [_] be able to change language-maybe
- [_] Allow tabs or spaces-maybe
- [_] Python (and other languages) improve syntax checking

### Plugins
- [_] New - Bookmark plugin
- [_] New - Help/reference plugin
- [_] Find - Grep like plugin (maybe combine with Find)
- [_] New - Spellcheck
- [x] New - scratch - just a textbox that saves with workspace
- [_] Preview - add find
- [_] Preview - show link in statusbar when hovering (maybe use current statusbar)
- [_] Filebrowser - copy file
- [_] Filebrowser - indicate if file is open
- [_] Filebrowser - be able to have multiple roots
- [_] Filebrowser - reload menu option
- [_] Filebrowser - grab path function
- [_] Filebrowser - search function
- [_] Filebrowser - run a file
- [_] Output - add menu and/or close option for output file
- [_] Output - be able to interactive
- [_] Install plugins from zip url
- [_] Python Shell - fix syntax highlighting
- [_] Python Shell - add autocomplete
- [_] open file selection overlay (sortable)