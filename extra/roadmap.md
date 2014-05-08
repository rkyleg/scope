# High Level Roadmap

# Current State
**Armadillo is almost ready for 1.0 release after a bit more testing**

### Features
- Cross Platform (Windows and Linux)
- Multiple language support
- Choice of multiple code editors: scintilla, ace, ckeditor
- Save workspaces (open files and filebrowser path)
- Run works for python, markdown, and html
- Outline plugin works for python, markdown, html, javascript, css, ini/conf

### Work in Progress
- Python shell plugin is a little buggy still
- minor syntax checking for Scintilla/Python would be nice.

# Armadillo 1.0
The Armadillo 1.0 release will be considered usable and will have the basic features that I want in an IDE.

- [x] Check and alert if open files have changed outside of editor
- [x] Fix most Python Shell querks
- [x] Finalize code layout structure (for editors, plugins, and other)
- [x] Finalize settings configuration and storage mechanism
- [x] Make sure robust for unicode errors (at least have error message on save/load)
- [x] No more updates to master branch until adequate testing has been done
- [x] Robust to most unicode errors

# Armadillo 2.0
Armadillo 2.0 will allow for better/easier user customization

- [ ] Ease of use of adding plugins and user customizeable plugins
- [-] UI for settings (maybe)
- [ ] More settings options
    - [x] User customizeable editors
- [ ] Improve Icon
- [ ] Continous checking and alert if open files have changed outside of editor
- [ ] Maybe more autocomplete functionality - if not to *heavy*

# Additional Features
Features that can be added independent of version

- [ ] Spellcheck plugin
- [x] Snippets plugin
- [x] Better documentation/integrated help (maybe as a plugin)