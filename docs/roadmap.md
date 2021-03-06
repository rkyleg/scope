# Scope - Roadmap
This roadmap contains details on where Scope is headed. The code structure is pretty stable as of version 0.7 and major changes are not anticipated.

## Philosophy
When adding features, Scope will attempt to adhere to the following ideals
- **lightweight** - keep lightweight and don't have a lot of features running for every edit
- **clean interface** - don't clutter main interface with lots of buttons
- **good utilization of screenspace** - make sure Scope works well on small screens (and large)
- **cross platform** - work on Linux, Windows, and Mac

## Features planned
*in no particular order or target date*
- Improve documentation including how to customize Scope and create plugins.
- Plugin app-like store with a central repository for plugins.  The plugin store would also show and manage plugin updates
- Some kind of update mechanism.  Scope will check for an update but then let the user choose when to update.
- Plugin dependency and version tracking
- Help plugin
- Better autocomplete for Python - probably using Jedi
- Convert to Python 3 and PyQt5 in 2017-2018

## Python 3 Support
Scope can only be run from source with Python 2.  Sometime in 2017-2018, Scope will convert to Python 3.  Due to limited development time, Scope will just convert to Python 3 and likely not support both.  Around the same time, Scope will also convert from Qt4 to Qt5.

Scope can still be used to code in Python 3.  Scope itself is just written in Python 2.  The command to run scripts can be edited in the Settings > Languages section.