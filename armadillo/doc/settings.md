<link rel="stylesheet" type="text/css" href="doc.css">

# [Home](start.html) | Settings

Settings are stored in the *.armadillo* folder in your user home directory.  Settings consist of:

- **workspaces folder** - saves the following settings for each workspace (json file).  )*do not modify the workspace files directly*)
    - Base path in file browser
    - Last opened files
    - What plugins and toolbars are visible
- **settings.conf** - this contains the main settings for Armadillo. You can edit this by clicking the ![](../img/wrench.png) button
- **window** - a binary file with window/plugin location settings

*Do not modify the default_settings.conf file as any updates to Armadillo will overwrite the settings here*

## settings.conf
The settings.conf file contains the main settings to customize Armadillo.  The file format is [ConfigObj](http://www.voidspace.org.uk/python/configobj.html)  - a modified ini.

### Notes
- 0 is considered false and 1 is considered true.
- Quotes are not needed for this settings file

### General settings
        view_folder=0
        save_workspace_on_close=1
        widgetstyle=plastique
        style=default
        activeEditors = ace,scintilla,ckeditor
        activePlugins = filebrowser,outline,py_console,find_replace,output,snippets,qt2py

- view_folder
    - view folder name in tab
    - default is 0
- save_workspace_on_close
    - save workspace settings on close (if this is set to 0, then you must use the Workspace Save menu to save the current workspace state)
    - default is 1
- widgetstyle
    - set the style of the editor (Qt style is used)
    - options are: windows, motif, cde, plastique, windowsxp, macintosh
    - default is plastique
- activeEditors
    - the list of active editors to load
- activePlugins - these are the plugins loaded on start

### Editor Settings
        [editors]
            [[ace]]
                wordwrap=0
                theme=twilight
                behavioursEnabled=1
                wrapBehavioursEnabled=1
                showWhitespace=0
            [[scintilla]]
                wordwrap=0
                autocomplete=1
                newLineMode=unix
                showWhitespace=0
            [[ckeditor]]

- editors
    - a dictionary of editors and their default settings
    - Not all editors use the same settings


### Favorite Languages (fav_lang)
        [[default]] # Default settings for all editors
            editor=scintilla
            wordwrap=0
        [[javascript]]
            editor=ace
            run=/home/convolutedlogic/nodejs/bin/node
            run_args=-i
        [[markdown]]
            editor=ace
            wordwrap=1

Different settings for the editor can be set for the default and each language.  If no parameter is specified, the default is used.  The double bracket indicates the language.  For the full list of languages look in the new menu for each editor.  The default for all languages is listed as `[[default]]`

The available (and default) parameters are:

- editor
    - what editor to use
    - scintilla,ace,ckeditor
- wordwrap
    - start in wordwrap mode
    - default = 0
- run
    - the run command to run
    - Ex: if you have node installed: run=/home/convolutedlogic/nodejs/bin/node
- run_args
    - a string of args to append to the run command (before the filename)
    - this is optional

The Ace editor has additional settings:

- theme
    - theme of editor
- behavioursEnabled
    - ace behavioiurs
    - default = 1
- wrapBehavioursEnabled
    - ace wrapBehaviours
    - default = 1
- fontSize
    - font size of editor
    - default = 12
- showPrintMargin
    - show the print margin
    - default = 0


### Extensions
        [extensions]
            py=python
            pyw=python
            js=javascript
            htm=html
            style=css
If you need to specify that a file extension goes with a specific language.

### Plugins
        
        [plugins]
            [[outline]]
                alwaysUpdate=0 # 1 to always update, 0 to update on save
        
            [[filebrowser]]
                showAll=0
                
            [[snippets]]
                path=/home/hdesktop/snippets
        
Specify settings for the look and naming of the plugins.  This is only for initial loading.  If you move the plugins around, the window state will be saved on close and this setting will be ignored.

- plugins - plugin specific settings