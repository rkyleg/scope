# TODO

## Armadillo Main
- [x] Check if files edited/saved outside of editor at least some of the time (menu option)
- [f] Check if files edited/saved outside of editor continous
- [f] Try to open in default editor, otherwise if language does not exist, try other editors
- [f] Add more language icons
- [ ] sys.argv file open work
- [x] Fix editor buttons checking if functions available
- [-] Save file uses extensions (with all option)
- [ ] Save as (save menu maybe)
- [x] if save or load fails - display message
- [-] if find not found - add statusbar message
- [x] improve statusbar save formatting
- [x] Workspace menu icons
- [x] Startpage not showing new favorites
- [ ] Have other Widgets that load in a new tab
- [x] Compile to exe
- [x] Add start like button to top to access menu
- [ ] DOCUMENTATION
- [x] BUG - if closing in zen mode - don't save window state

### Startpage
- [x] Update theme

### Settings
- [ ] Save settings in separate location (load defaults first)
- [ ] Themes - dark one
- [ ] Save settings for each editor and outline???
- [ ] Settings button can load 
- [ ] Settings page like webview (use alpaca)?
- [x] Native or plastique style
- [ ] have default settings in __init__ of each editor/plugin
- [ ] have settings folder - in main directory?? or use user directory
- [ ] option to store settings in os or with editor folder

## Editors
- [ ] Editor specific plugins view?
- [ ] Hide editors - store open editors with a file?
- [ ] Add Monkey
- [ ] Store wordwrap preferences with language
- [ ] Show line/column numbers in status bar

### Monkey
- [f] pen monkey file type
- [f] get rid of projects tab
- [f] Run will update preview

## CKEditor
- [x] Add text alignment
- [x] Check for text changed (asterix to tab)

### Scintilla
- [ ] Fix autocomplete when hitting any key (set to return or tab only)
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

## Plugins
- [ ] Snippets plugin
- [ ] Spellcheck plugin
- [ ] Help plugin (with search, maybe based on current file language)
- [ ] Python code editor to run on current tab
- [ ] Simple git plugin (commit, push, pull, diff stats,launch diff tool)

### Outline
- Languages
 - [x] Markdown
- [f] Use themes for color coding
- [-] Right click refresh
- [f] toggle autorefreshing
- [x] ctrl+o to show outline

### Python Shell
- [x] Fix mouse cursor messing up code
- [ ] Auto complete would be nice
- [x] syntax highlighting
- [ ] Fix selection replace/delete bug

### File Browser
- [x] Return press opens folder
- [ ] toggle to view all files
- [x] be able to launch file with os default (do this for unknown extensions on double click)
- [x] right click new file (select from extensions
- [x] delete file option
- [ ] Reload option
- [x] rename file (also has to rename if file open in editor or at least check first)
- [f] collapse all/expand all
- [x] Fix extra / in tab name hover (in Linux at least)
- [f] Goto current file/tab
- [x] Double click toggles expand
- [x] Improve tree formatting

### Output
- [x] Add markdown to run (use javascript preview with webview - or see markdown2)
- [f] Create markdown viewer

## Other Random TODO
- [ ] Add Preview editor/widget that is tied to another editor and can refresh (markdown, html)
- [ ] Add other widgets as tabs (that aren't editors)
