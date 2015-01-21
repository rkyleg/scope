<link rel="stylesheet" type="text/css" href="doc.css">

# [Home](start.html) | Plugins
Armadillo comes with standard plugins to the left and bottom of the editor window. Custom plugins can be created.

## Standard Plugins

- **File Browser** - Browse the workspace directory.
    - Right click for a menu with file browser options
    - To edit the path, just click on the path, edit and press return. The last path used will be stored with the workspace.

- **[Outline](plugins_outline.md)** - Outline of code structure

- **Find/Replace** - Common find/replace functions

- **[Output](plugins_output.md)** - Displays output of running file (only works for Python)

- **[Python Shell](plugins_pyconsole.md)** - An interactive Python shell

- **Snippets** - view/store snippets of code
    - You can set an existing directory of snippets in the settings
        
            [plugins]
                [[snippets]]
                    path=/home/username/scripts

- **Preview** - a built in WebKit webbrowser for previwing html and markdown. A file does not need to be saved to use the preview.


- **PyQt Converter** - Convert Qt Designer ui files to python. *This plugin is not active by default*


## Select Active Plugins
To specify which plugins are active, edit the **activePlugins** key of the General Settings. Use the foldername of the plugins and separate by commas.

        activePlugins = filebrowser,outline,py_console,find_replace,output,snippets,preview,qt2py

## Custom Plugins
You can create your own plugins with Python and PyQt.

1. Create a new directory for your plugin in /armadillo/plugins
2. Create a \_\_init\_\_.py file with a function called **addPlugin(armadillo)**
3. Return a QWidget from the addPlugin function
4. The QWidget must have a title and location (left or bottom) attribute.
5. Make the plugin active by adding the foldername of the plugin to the activePlugins key of the settings (comma separated).

### Example of a custom Plugin
To create a plugin called 'test', create a folder named test in plugins directory that would yield: /armadillo/plugins/test.

\_\_init\_\_.py file in the test folder would look like:
    
        from PyQt4 import QtGui, QtCore
        def addPlugin(armadillo):
            plugin = QtGui.QWidget()
            plugin.title='Test'
            plugin.location='left'
            return plugin