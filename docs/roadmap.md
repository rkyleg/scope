# [Scope Documentation](index.md) |  Scope Roadmap
Details on where Scope is headed.  Scope is currently considered an alpha state (version 0.3.x).

## Philosophy
When adding features, Scope will attempt to adhere to the following ideals
- **lightweight** - keep lightweight and don't have a lot of features running for every edit
- **clean interface** - don't clutter main interface with lots of buttons
- **utilize screenspace** - make sure Scope works well on small screens
- **cross platform** - must work on Windows, Linux, and Mac

## Near term features planned
- replacing config file with a nice settings interface
- adding a plugin management interface that will allow installing plugins from a web link or a zip file
- Create binaries for Windows and maybe Linux
- Check for file changes outside of Scope continuously
- Lock down API - stop making changes and have a good API for creating plugins
- Good documentation on using and creating plugins

## Longer term features planned
- Create binaries for Mac
- Plugin update mechanism
- Plugin dependency and version tracking
- Help plugin
- better autocomplete for Python

## Python 3 Support
Scope can only be run from source with Python 2.  Sometime in 2016-2018, Scope will convert to Python 3.  Due to limited development time, Scope will just convert to Python 3 and not support both.  Around the same time, Scope will also convert from Qt 4.8 to Qt 5.latest.