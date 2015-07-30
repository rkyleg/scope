document.onkeydown = keydown
function keydown (event) {
    // event = event || window.event
    file_items = document.getElementsByClassName('file')
    file_active=document.getElementsByClassName('file current')
    if (file_active.length > 0) {
        for (var i=0; i < file_items.length;i++) {
            if (file_items[i].className == 'file current') {
                file_active=i
            }
        }
        // file_active = parseInt(document.getElementsByClassName('file current')[0].id)
        // file_active = file_items.indexOf(document.getElementsByClassName('file current')[0])
        prev_active = document.getElementsByClassName('file current')[0]
        // prev_active = file_active
    }
    else {file_active=''}
    ok=0
    if (event.keyCode==27) {
        //escape
        HUD.closeHUD()
    }
    else if (event.keyCode==37) {
        // left
        file_active -=1
        ok=1
    }
    else if (event.keyCode==39) {
        // right
        file_active +=1
        ok=1
            
    }
    else if (event.keyCode==13) {
        // return
        opentab(file_items[file_active].id)
    }
    if (ok==1){
        // Go back to beginning if at end
        if (file_active >= file_items.length) {
            file_active=0
        }
        // Go to end if at beginning
        else if (file_active < 0) {
            file_active = file_items.length-1
        }
        
        // Update style and set focus
        highlighttab(file_items[file_active].id)
        // file_items[file_active].className='file current'
        // file_items[file_active].focus()
        // prev_active.className='file'
        
    }
}

function closetab(id) {
    elm = document.getElementById(id)
    elm.parentNode.removeChild(elm)
}

function opentab(id) {
    HUD.opentab(id)
}
function highlighttab(id) {
    // Get previous highlight
    active_items = document.getElementsByClassName('file current')
    if (active_items.length>0) {
        prev_active = active_items[0]
        prev_active.className='file'
    }
    
    // Highlight tab with id
    document.getElementById(id).className='file current'
    document.getElementById(id).focus()
}