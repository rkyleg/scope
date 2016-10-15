/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';
    // Se the most common block elements.
    config.format_tags = 'p;h1;h2;h3;pre';

    // Make dialogs simpler.
    config.extraPlugins = 'class_edit';
    config.removeDialogTabs = 'image:advanced;link:advanced';
    config.removePlugins='preview'
    config.removeButtons='Styles'
    
    // customization
    config.enterMode = CKEDITOR.ENTER_BR;
    config.allowedContent = true
    
    config.toolbarGroups = [
    { name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
    { name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
    { name: 'styles' },
    { name: 'links' },
    { name: 'insert' },
    { name: 'forms' },
    { name: 'tools' },

    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
    { name: 'paragraph',   groups: [ 'list','blocks',  ] },
    { name: 'paragraph2',   groups: [ 'indent', 'align' ] },
    
    { name: 'colors' },
    { name: 'document',    groups: [ 'mode', 'document', 'doctools' ] },
    { name: 'others' },
    { name: 'about' }
];
    
};
