# High Level Roadmap

# Current State

### Features
- Cross Platform (Windows and Linux)
- Multiple language support
- Choice of multiple code editors: scintilla, ace, ckeditor
- Save workspaces (open files and filebrowser path)
- Run works for python, markdown, and html
- Outline plugin works for python, markdown, html, javascript, css

### Work in Progress
- Python shell plugin is buggy
- I keep changing the settings file and layout that is not backwards compatible
- I will probably change the code structure

# Armadillo 1.0
The Armadillo 1.0 release will be considered usable and will have the basic features that I want in an IDE.

- [ ] Check and alert if open files have changed outside of editor
- [ ] Fix Python Shell querks
- [ ] Finalize code layout structure (for editors, plugins, and other)
- [ ] Finalize settings configuration and storage mechanism
- [ ] Make sure robust for unicode errors (at least have error message on save/load)
- [ ] No more updates to master branch until adequate testing has been done

# Armadillo 2.0
Armadillo 2.0 will allow for better/easier user customization

- [ ] Ease of use of adding plugins and user customizeable plugins
- [ ] UI for settings
- [ ] More settings options
    - [ ] User customizeable editors
- [ ] Improve Icon

# Additional Features
Features that can be added independent of version

- [ ] Spellcheck plugin
- [ ] Snippets plugin
- [ ] Better documentation/integrated help (maybe as a plugin)