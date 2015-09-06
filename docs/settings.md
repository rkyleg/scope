<link rel="stylesheet" type="text/css" href="docs.css">

# [Scope Documentation](index.md) | Settings

Settings are stored in the *.scope* folder in your user home directory.  Settings consist of:

- **settings.conf** - this contains the main settings for Scope. You can edit this by clicking the <img src="../style/img/settings.png" style="max-height:16px;background:rgb(70,70,70);padding:2px;"> button on the left toolbar
- **workspaces folder** - saves the following settings for each workspace (json file).  (*do not modify the workspace files directly*)
    - Base path in file browser
    - Last opened files

*Do not modify the default_settings.conf file as any updates to Scope will overwrite the settings here*

## ![](../style/img/wrench.png) settings.conf
The settings.conf file contains the main settings to customize Scope.  The file format is [ConfigObj](http://www.voidspace.org.uk/python/configobj.html)  - a modified ini.

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
    - view parent folder name in tab along with filename
    - default is 0
- save_workspace_on_close
    - save workspace settings on close (if this is set to 0, then you must use the Workspace Save menu to save the current workspace state)
    - default is 1
- widgetstyle
    - set the style of the editor (Qt style is used)
    - options are: windows, motif, cde, plastique, windowsxp, macintosh
    - default is plastique
    - leave blank to use OS default (widgetstyle=)
- activeEditors
    - the list of active editors to load
- activePlugins - these are the plugins loaded on start

### Window Settings
        [window]
            openMode=1
            [[size]]
                width=100%
                height=100%
            [[margin]]
                left=50
                right=50
                top=50
                bottom=50 
            
            # Plugin Window settings
            [[pluginLeft]]
                width=260
                visible=1
                tabPosition=top
                showTabText=0
            [[pluginBottom]]
                visible=1
                height=180
                showTabText=1
            [[pluginRight]]
                visible=0
                width=50%
                tabPosition=bottom
                showTabText=1
                leftToggle=1 # Hide left plugins when right plugin toggled (show left when right is hidden)

- openMode - size the editor opens as
    - 1 = custom - use size and margin attributes
    - 2 = maximize window
- pluginLeft, pluginBottom, pluginRight
    - visible 
        - 1 = visible
        - 0 = hidden by default (can be made visible through the Main Menu > Window menu
    - width/height - specify default width or height the plugin window is opened to

### Editor Settings
Default settings for the editors. These settings are overwritten by language specific settings (if set).  See Programming Languages below.

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
                showWhitespace=0
                fontFamily=Courier
                fontSize=10
            [[ckeditor]]

- editors
    - a dictionary of editors and their default settings
    - Not all editors use the same settings
- **Ace Editor** has additional settings:
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


### Programming Languages (prog_lang)
Programming language specific settings. Set theme and editor for each language. If no parameter is specified, the default is used.  The double bracket indicates the language.  For the full list of languages available to each editor, look in the new menu for each editor.  The default settings for all languages not specified is listed as `[[default]]`

        [prog_lang]
            [[default]] # Default settings for all editors
                editor=scintilla
                wordwrap=0
            [[python]]
                run=python -u
            [[javascript]]
                editor=ace
                run=/home/convolutedlogic/nodejs/bin/node -i
            [[markdown]]
                editor=ace
                wordwrap=1
            [[ini]]
                editor=ace
                theme=vibrant_ink
                fave=0  # default is 1

The available (and default) parameters are:

- editor
    - what editor to use
    - scintilla,ace,ckeditor
- wordwrap
    - start in wordwrap mode
    - default = 0
- run
    - the command to run (dos or shell command) which is passed the filename.
    - you can add arguments with the command like -u to make Python print as it goes instead of at the end.
    - Special Commands - there are some reserved commands that perform a specific function in Scope.
        - *preview* - html and markdown use this by default to load in the split preview plugin.
        - *webbrowser* - use this command to launch the file in your default web browser.
    - Example: if you have node installed you can set your path to node:
            *run=/home/convolutedlogic/nodejs/bin/node -i*
- fave
    - considered a favorite language and shows up in New menu and on home page and HUD
    - this defaults to true (1) if not specified. set to 0 to not show in new menu

You can also customize the editor settings like theme, showPrintMargin (for Ace Editor) for each language. Use the same keys/values as listed for the editor's settings.


### Extensions
If you need to specify that a file extension goes with a specific language (languages are defined by the editor).

        [extensions]
            py=python
            pyw=python
            js=javascript
            htm=html
            style=css
            conf=ini

### Plugins
Settings specific to each plugin, that the plugins can use.

        [plugins]
            [[outline]]
                alwaysUpdate=0 # 1 to always update, 0 to update on save
        
            [[filebrowser]]
                showAll=0
                defaultPath= # Default path to open (leave blank to open to user home directory)
                externalFileBrowser=C:\portableapps\explorer++.exe  # to use a specific file browser when launching externally, specify program here
                
            [[snippets]]
                path=/home/hdesktop/snippets
