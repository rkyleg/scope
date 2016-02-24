CKEDITOR.plugins.add( 'class_edit', {
    init: function( editor ) {
    
        editor.addCommand( 'editClass',new CKEDITOR.dialogCommand( 'editClassDialog' ) );
        
        // Add a dialog window definition containing all UI elements and listeners.
        CKEDITOR.dialog.add('editClassDialog', function(editor) {
            return {
                title : 'Edit Class',
                width : 200,
                height : 80,
                contents: [{
                    id: 'MainTab',
                    label: 'Properties',
                    elements:[
                        {
                            type:'html',
                            html:'placeholder',
                            id:'elm_name',
                        },
                        {
                            type: 'text',
                            id: 'class_value',
                            label: 'Class',
                            setup: function(element){
                                cls=element.getAttribute('class')
                                this.setValue(cls);
                            }
                        },
                       
                    ]
                }],
                onShow : function(){
                    var dialog = this
                    var elm= this.getParentEditor().getSelection().getStartElement()
                    if (elm) {
                        this.setupContent(elm)
                        helm = dialog.getContentElement('MainTab','elm_name').getElement()
                        helm.setHtml('&lt;'+elm.getName()+'&gt;')
                    }
                },
                
                onOk : function() {
                    var dialog = this
                    var elm = editor.getSelection().getStartElement()
                    elm.setAttribute('class',dialog.getValueOf('MainTab', 'class_value' ).trim())
                }
            }
        })
    
        /* Add to Context Menu */
        if (editor.contextMenu) {
            editor.addMenuGroup('more')
            editor.addMenuItem( 'classEditItem', {
                label:'Edit Class',
                icon:'',
                command:'editClass',
                group:'more'
            })
        }
        
        /* Listener for Context Menu Type */
        if (editor.contextMenu) {
            editor.contextMenu.addListener(function(element) {
                // console.log(element.getName())
                if (element && !element.isReadOnly() && !element.data( 'cke-realelement') && element.getName()!='body')
                return {classEditItem : CKEDITOR.TRISTATE_OFF}
            })
        }
    
    
    }
})