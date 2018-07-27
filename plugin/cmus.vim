if has('win32')
    "only unix/linux/macos are supported by vim-cmus!
    finish
endif

function! s:cmus_query(verb)
    let l:status  = '' " playing, paused, ...
    let l:artist  = ''
    let l:title   = ''
    let l:album   = ''
    let l:track   = '' " track number
    let l:date    = ''
    let l:file    = '' " file name
    let l:stream  = '' " for radio or other streaming services

    let l:result = system('cmus-remote ' . a:verb)
    let l:lines = split(l:result, '\n')
    for l:line in l:lines
        if empty(l:status)
            let l:status = matchstr(l:line, '\vstatus\s+\zs(.*)')
        endif
        if empty(l:artist)
            let l:artist = matchstr(l:line, '\vartist\s+\zs(.*)')
        endif
        if empty(l:album)
            let l:album = matchstr(l:line, '\valbum\s+\zs(.*)')
        endif
        if empty(l:title)
            let l:title = matchstr(l:line, '\vtitle\s+\zs(.*)')
        endif
        if empty(l:track)
            let l:track = matchstr(l:line, '\vtracknumber\s+\zs(.*)')
        endif
        if empty(l:date)
            let l:date = matchstr(l:line, '\vdate\s+\zs(.*)')
        endif
        if empty(l:file)
            let l:file = matchstr(l:line, '\vfile\s+\zs(.*)')
        endif
        if empty(l:stream)
            let l:stream = matchstr(l:line, '\vstream\s+\zs(.*)')
        endif
    endfor

    " make a list of sub-items to be displayed
    let l:list = [l:status, ': ']
    if !empty(l:stream)
        call add(l:list, l:stream)
        if !empty(l:title)
            call extend(l:list, [' [stream: ', l:title, ']'])
        endif
    elseif empty(l:artist) && empty(l:title) " propably file has no meta/tag information
        call add(l:list, l:file)
    else " playing local file, with some possible tags
        if !empty(l:artist)
            call extend(l:list, [l:artist, ' - '])
        endif
        if l:track
            call extend(l:list, [l:track, ') '])
        endif
        if !empty(l:title)
            call add(l:list, l:title)
        else
            call add(l:list, 'untitled')
        end
        if !empty(l:album)
            call extend(l:list, [' [', l:album, ']'])
        endif
        if l:date
            call extend(l:list, [' @', l:date])
        endif
    endif
    echom join(l:list, '')
endfunction

function! s:cmus_set(setting)
    silent execute '!cmus-remote ' . '--raw ' . "'set " . a:setting . "'"
endfunction

function! s:cmus_current()
    call s:cmus_query("-Q")
endfunction

function! s:cmus_previous()
    call s:cmus_query("--prev -Q")
endfunction

function! s:cmus_next()
    call s:cmus_query("--next -Q")
endfunction

function! s:cmus_pause()
    call s:cmus_query("--pause -Q")
endfunction

function! s:cmus_play()
    call s:cmus_query("--play -Q")
endfunction

function! s:cmus_stop()
    call s:cmus_query("--stop -Q")
endfunction

function! s:cmus()
    echo "cmus options:\n"
                \ "i. information\n"
                \ "z. previous\n x. play\n c. pause\n"
                \ "v. stop\n b. next\n"
                \ "l. play all mode\n t. play artist mode\n m. play album mode\n"
    let opt = nr2char(getchar())
    if opt == 'i'
        call s:cmus_current()
    elseif opt == 'z'
        call s:cmus_previous()
    elseif opt == 'x'
        call s:cmus_play()
    elseif opt == 'c'
        call s:cmus_pause()
    elseif opt == 'v'
        call s:cmus_stop()
    elseif opt == 'b'
        call s:cmus_next()
    elseif opt == 'l'
        call s:cmus_set('aaa_mode=all')
    elseif opt == 't'
        call s:cmus_set('aaa_mode=artist')
    elseif opt == 'm'
        call s:cmus_set('aaa_mode=album')
    endif
endfunction

command! Cmus         call s:cmus()
command! CmusCurrent  call s:cmus_current()
command! CmusPrevious call s:cmus_previous()
command! CmusPlay     call s:cmus_play()
command! CmusPause    call s:cmus_pause()
command! CmusStop     call s:cmus_stop()
command! CmusNext     call s:cmus_next()
