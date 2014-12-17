# TODO

## Armadillo Main
- [x] Check if files edited/saved outside of editor at least some of the time (menu option)
- [f] Check if files edited/saved outside of editor continous
- [x] Try to open in default editor, otherwise if language does not exist, try other editors
- [f] Add more language icons
- [x] sys.argv file open work
- [x] Fix editor buttons checking if functions available
- [-] Save file uses extensions (with all option)
- [x] Save as (save menu maybe)
- [x] if save or load fails - display message
- [-] if find not found - add statusbar message
- [x] improve statusbar save formatting
- [x] Workspace menu icons
- [x] Startpage not showing new favorites
- [f] Have other Widgets that load in a new tab
- [x] Compile to exe
- [x] Add start like button to top to access menu
- [x] BUG - if closing in zen mode - don't save window state
- [x] check if extension = language if not found elsewhere
- [x] merge default settings and user settings
- [x] Load workspace closes open files
- [x] Save As
- [] show column number and wordcount, total lines? - stats in statusbar
- [x] Make sure default editor settings (wordwrap,etc) are loading correctly
- [x] Print
- [] compile option (need args as option)
- [-] add run with args menu
- [] Add header comment button (use outline protocol)
- [] save splitter state
- [] info (word count, column row,) function
- [] save recent files if no workspace open (still open home first) - or view recent files somehow
- [] be able to change language

### Startpage
- [x] Update theme
- [x] Create light theme
- [x] add new workspace button to home page
- [] update home page after new workspace (if current tab)

### Documentation
- [x] Just use markdown viewer
- [x] Update settings documentation
- [] py console documentation (armadillo object)
- [] improve settings documentation

### Workspaces
- [] save last file open
- [x] close workspace

### Settings
- [x] Save settings in separate location (load defaults first)
- [f] Themes - dark one
- [x] Save settings for each editor and outline???
- [x] Settings button can load 
- [f] Settings page like webview (use alpaca)?
- [x] Native or plastique style
- [-] have default settings in __init__ of each editor/plugin
- [x] have settings folder - in main directory?? or use user directory
- [f] option to store settings in os or with editor folder
- [x] add stylesheet to settings (add error checking)
- [-] make plugins visible if added for the first time - if possible
- [] save splitter state
- [] save editor used to open file with workspace
- [] recent file list (include or not workspaces - or list recent workspaces)
- [] fav_lang settings change to lang, make fav_lang just a list
- [] fix config file not loading integers correctly

## Editors
- [] Editor specific plugins view?
- [] Hide editors - store open editors with a file?
- [] Add Monkey
- [x] Store wordwrap preferences with language
- [f] Show column numbers in status bar
- [] Allow tabs or spaces

### Monkey
- [f] pen monkey file type
- [f] get rid of projects tab
- [f] Run will update preview

### CKEditor
- [x] Add text alignment
- [x] Check for text changed (asterix to tab)

### Scintilla
- [-] Fix autocomplete when hitting any key (set to return or tab only)
- [x] Add Icon
- [f] check line syntax

### Ace
- [x] Ctrl S save
- [x] Fix cursor alignment problem (check in Linux - font-family style change fixes)
- [x] Indent buttons
- [x] Check save
- [x] toggle comment
- [x] copy/paste from other tools
- [x] custom right click menu for extra options (add copy and paste to it)
- [x] edit themes
- [x] replace/replaceall
- [x] goto
- [x] Fix cut keyboard shortcut
- [f] Add Split view
    - [f] option for previewer split (html and markdown)
- [-] Add find tag/branch function
- [x] When opening start at cursor position 1
- [x] Right click edit behaviours
- [x] disable drag and drop in webpage
- [x] add autocomplete
- [x] fix find/replace with a '
- [] add javascript custom settings
- [] wrap to 

### Webview
- [x] if markdown, generate
- [x] move markdown outside of output


## Plugins
- [x] Snippets plugin
- [f] Spellcheck plugin
- [f] Help plugin (ctrl h) with dropdown of websites to search (google, stack overflow, duckduck go, etc), maybe based on current file language
- [f] Python code editor to run on current tab - possible split with shell (little code editor)
- [f] Simple git plugin (commit, push, pull, diff stats,launch diff tool)
- [] update plugin style
- [] new plugin - open files plugin (sort by type)
- [] bookmark plugin (have categories, searchable)

### Outline
- Languages to add
    - [x] Markdown
- [f] Use themes for color coding
- [x] Right click refresh (ctrl+o instead)
- [-] toggle autorefreshing
- [x] ctrl+o to show outline
- [x] Delete pages when closing tabs
- [x] search outline
- [x] Highlight current section closest to top of screen
- [x] Move outline code to language plugins in separate files
- [x] Way to turn off
- [x] Test Handling large blocks of text
- [x] Option to update only on save (or by default)
- [x] Refresh right click menu
- [] Other that grabs --- comments

### Python Console
- [x] Fix mouse cursor messing up code
- [f] Auto complete would be nice
- [f] upon import - add completion to editor
- [x] syntax highlighting
- [x] Fix selection replace/delete bug
- [] Fix syntax highlighting of strings (and brackets mixed with strings)
- [x] Add python2.7 source if installed

### File Browser
- [x] Return press opens folder
- [x] toggle to view all files
- [x] be able to launch file with os default (do this for unknown extensions on double click)
- [x] right click new file (select from extensions
- [x] delete file option
- [x] rename file (also has to rename if file open in editor or at least check first)
- [f] collapse all/expand all
- [x] Fix extra / in tab name hover (in Linux at least)
- [f] Goto current file/tab
- [x] Double click toggles expand
- [x] Improve tree formatting
- [x] create new file in main directory
- [ ] copy file
- [x] New folder
- [ ] indicate if file is open
- [ ] be able to have multiple roots
- [] reload menu option
- [] filebrowser grab path function
- [] search in file browser
- [] run option to filebrowser

### Output
- [x] Add markdown to run (use javascript preview with webview - or see markdown2)
- [x] Create markdown viewer
- [x] switch to main markdown package
- [x] add markdown preview
- [f] have additional markdown settings based on markdown-python extras
- [x] markdown compile
- [x] allow running multiple outputs - add tabs for each and stop button
- [x] goto correct output tab when switching tabs
- [f] when closing a file, will need to stop output
- [x] Move markdown and preview to separate files for customization
- [] add menu and/or close option for output file
- [] custom output command
- [] be able to write to output

### Snippets
- [x] search
- [x] list of snippets
- [x] show code with formatting (scintilla for now)
- [x] edit/save snippets
- [x] use settings for snippets location (home default)
- [f] search within files
- [x] double click to copy to clipboard

## Other Random TODO
- [x] Add Preview editor/widget that is tied to another editor and can refresh (markdown, html)
- [] Add other widgets as tabs (that aren't editors)

## Binaries
- [x] Create Windows binary
- [] check if python and qt installed when launching binary - remove pyqt converter if not
- [x] Create Linux binary
- [] Create Mac binary