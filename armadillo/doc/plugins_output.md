<link rel="stylesheet" type="text/css" href="doc.css">

# [Home](start.html) | [Plugins](plugins.md) | Output

The Output plugin will run code and display any output from the code. The appropriate tools for the language need to be installed along with modifications to the settings file. Multiple files can be running at once in a separate process.

# Screen Overview
![](img/plugin_output.png)

# Setup your language to run
1. Click the settings button ![](../img/wrench.png) to edit your settings.
2. In the fav_lang section, add/edit the run and run_args (optional) attributes to the language

        [fav_lang]
            [[python]]
                run=python -u

    - The run argument contains the command or path to the executable to run your code against.
    - Include additional arguments at the end. For Python -u makes the output update as the code runs instead displaying only when it finishes.

3. Before executing the code, the current directory is changed to the file being run.
4. The command is built as:

        <run> <filename>
        python -u test.py

# How to Run Code
1. Make sure appropriate software is installed and settings are setup as described above.
2. Click the run button ![](../img/tri_right.png) in the top toolbar to execute the code.

# Examples of other Language Settings

        [fav_lang]
            # Javascript/Node
            [[javascript]] 
                run=/home/username/nodejs/bin/node -i
            
            # CoffeeScript
            [[coffee]] 
                run=coffee -p --print

*Appropriate software needs to be installed before this will work.*