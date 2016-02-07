if !has('python')
    finish
endif

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )

function! s:call_python(verb)
python << endpython
import sys
import vim
sys.argv = ['vim_mode', vim.eval("a:verb")]
endpython
    execute 'pyfile ' . s:script_folder_path . '/cmus.py'
endfunction

function! s:cmus_current()
    call s:call_python("curr")
endfunction

function! s:cmus_previous()
    call s:call_python("prev")
endfunction

function! s:cmus_next()
    call s:call_python("next")
endfunction

function! s:cmus_pause()
    call s:call_python("pause")
endfunction

function! s:cmus_play()
    call s:call_python("play")
endfunction

function! s:cmus_stop()
    call s:call_python("stop")
endfunction

function! Cmus()
    echo "cmus options:\n"
                \ "i. information\n"
                \ "z. previous\n x. play\n c. pause\n"
                \ "v. stop\n b. next\n"
                \ "a. all mode\n t. artist mode\n m. album mode\n"
    let opt = nr2char(getchar())
    if opt == 'i'
        call s:call_python('curr')
    elseif opt == 'z'
        call s:call_python('prev')
    elseif opt == 'x'
        call s:call_python('play')
    elseif opt == 'c'
        call s:call_python('pause')
    elseif opt == 'v'
        call s:call_python('stop')
    elseif opt == 'b'
        call s:call_python('next')
    elseif opt == 'l'
        call s:call_python('all')
    elseif opt == 't'
        call s:call_python('artist')
    elseif opt == 'm'
        call s:call_python('album')
    endif

endfunction

command! Cmus call Cmus()
command! CmusCurrent call s:cmus_current()
command! CmusPrevious call s:cmus_previous()
command! CmusNext call s:cmus_next()
command! CmusPause call s:cmus_pause()
command! CmusPlay call s:cmus_play()
command! CmusStop call s:cmus_stop()
