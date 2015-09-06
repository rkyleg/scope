<link rel="stylesheet" type="text/css" href="docs.css">

# [Scope Documentation](index.md) | Editors
Scope comes with multiple code editors, so you can choose the one you want for each language.

- [QScintilla](http://www.riverbankcomputing.com/software/qscintilla/intro) - QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control. As well as features found in standard text editing components, QScintilla includes features especially useful when editing and debugging source code.
    - Scope uses this as default for Python and text files
    - Scintilla uses less memory

- [Ace](http://ace.c9.io/) - Ace is an embeddable code editor written in JavaScript. It matches the features and performance of native editors such as Sublime, Vim and TextMate.
    - Scope uses this by default for html, css, markdown, and javascript
    - Ace has built in syntax checking for html, css, and javascript

- [CKEditor](http://ckeditor.com/) - CKEditor is a ready-for-use HTML text editor designed to simplify web content creation. It's a WYSIWYG editor that has common word processor features to generate html.
    - CKEditor is less of a code editor, but can be useful for creating content in html.

## Why Multiple?
There are pros and cons to each editor. Scintilla uses less resources and is my default for Python. Ace has better built in tools for html, javascript, and css, but uses more resources. Ace also supports more languages. CKEditor provides a nice WYSIWYG interface for creating some simple documents. You can disable an editor by editing the activeEditors attribute in the settings.