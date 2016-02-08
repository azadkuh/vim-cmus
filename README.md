# vim-cmus
vim-cmus: control [cmus](https://cmus.github.io/) music player directly from vim

`cmus` is a small, fast, **No Nonsense** and powerful console music player for Unix-like operating systems.

This plugin helps you to control cmus right from your vim/gvim/macvim.

`vim-cmus` requires python (2.7 or higher) to operate.


## screen cast
![vim-cmus](https://cloud.githubusercontent.com/assets/6501462/12872205/60b97712-cdb1-11e5-8e0b-f952a41c5f90.gif)

## installation
Use you favourite vim plugin manager, [vundle](https://github.com/VundleVim/Vundle.vim) for example, and add:
```
" cmus remote control
Plugin 'azadkuh/vim-cmus'
```

You can optionally add following mappings to your `.vimrc`:
```
" cmus controls
nnoremap <leader>i :CmusCurrent<cr>
nnoremap <leader>z :CmusPrevious<cr>
nnoremap <leader>x :CmusPlay<cr>
nnoremap <leader>c :CmusPause<cr>
nnoremap <leader>v :CmusStop<cr>
nnoremap <leader>b :CmusNext<cr>
```

## optional bidi
**Optionally**, if your music collection contains unicode strings esp in RTL (right to left) languages as Persian, Hebrew, Arabic, ... please install [pyfribidi](https://pypi.python.org/pypi/pyfribidi/) to help `vim-cmus` render bi-directional text (where the cmus itself fails to render them properly! as shown in the sample screen cast)

to Install `pyfribidi`:
```bash
$> sudo pip install pyfribidi
```
by [pip](https://pip.pypa.io/en/stable/installing/) or any other python package manager.


## command list
at the moment following commands are implemented:
```
" shows an interactive menu to send a command to cmus remotely
:Cmus

" shows the information of current song
:CmusCurrent

" commands to controll cmus player
:CmusPrevious
:CmusNext
:CmusPlay
:CmusPause
:CmusStop
```

