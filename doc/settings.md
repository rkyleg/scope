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

- activePlugins
    - the list of active plugins to load

- editors
    - the list of active editors to load

### Favorite Languages (fav_lang)
Different settings for the editor can be set for the default and each language.  The available (and default) parameters are:

- editor
    - what editor to use
    - scintilla,ace,ckeditor
- wordwrap
    - start in wordwrap mode
    - default = 0
- theme
    - theme of editor (currently only works for ace - other editors ignore)
- behavioursEnabled
    - ace behavioiurs (currently only works for ace - other editors ignore)
    - default = 1
- wrapBehavioursEnabled
    - ace wrapBehaviours (currently only works for ace - other editors ignore)
    - default = 1

### Extensions
If you need to specify that a file extension goes with a specific language.

### Plugins
Specify settings for the look and naming of the plugins.  This is only for initial loading.  If you move the plugins around, the window state will be saved on close and this setting will be ignored.

- dockarea
    - what section of the screen should it load by default.
- title
    - the title that shows up in the tab for the plugin.