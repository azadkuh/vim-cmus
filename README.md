# vim-cmus
`vim-cmus`:  [cmus](https://cmus.github.io/)  directly from *vim*/*neovim*.

> *cmus* is an small, fast, **no nonsense** and powerful console music player
  for unix-like operating systems.

This plugin helps you to control *cmus* right from your vim/neovim/gvim/macvim
session.

## features

- `vim-cmus` is a single vim script and does not depend on python or any other
  runtime *(new versions do not need python as requirement anymore)*
- shows meta/tag information of current file/stream of *cmus*, including:
  stream info, title, artist, album, track number, date, file name, ...
- supports control commands: previous, play, pause, stop and next
- supports setting `aaa_mode`: all, album and artist


## screen shots
`:Cmus` as a command, shows an interactive menu:

![vim-cmus](https://user-images.githubusercontent.com/6501462/43317561-845a717c-91b2-11e8-92dd-0bf27db6d9df.png)

`:CmusCurrent` to echo current **file** playing by *cmus*:

![vim-cmus](https://user-images.githubusercontent.com/6501462/43317571-907b82d4-91b2-11e8-966b-ca709812d65c.png)

or current **stream** playing by *cmus*:

![vim-cmus](https://user-images.githubusercontent.com/6501462/43317590-9cb2335e-91b2-11e8-877b-8a62f2d595ee.png)

or

![vim-cmus](https://user-images.githubusercontent.com/6501462/43317598-a620ded6-91b2-11e8-8df3-03bbc059505b.png)


## installation
by your favourite vim plugin manager:

- [vim-plug](https://github.com/junegunn/vim-plug)
```
" cmus remote control
Plug 'azadkuh/vim-cmus'
```

- [vundle](https://github.com/VundleVim/Vundle.vim)
```
" cmus remote control
Plugin 'azadkuh/vim-cmus'
```

obviously you need [`cmus`](https://cmus.github.io/) itself to be
installed. to check it, please try:

```bash
# must be accessible from your ${PATH}
$> cmus-remote -Q
```

## command list
at the moment following commands are implemented:

- `:Cmus`
  shows an interactive menu to send a command to cmus remotely
- `:CmusCurrent`
  shows the information of current song

- `:CmusPrevious`
- `:CmusPlay`
- `:CmusPause`
- `:CmusStop`
- `:CmusNext`



You can optionally add following mappings to your `.vimrc`:
```vim
" cmus controls
nnoremap <leader>i :CmusCurrent<cr>
nnoremap <leader>z :CmusPrevious<cr>
nnoremap <leader>x :CmusPlay<cr>
nnoremap <leader>c :CmusPause<cr>
nnoremap <leader>v :CmusStop<cr>
nnoremap <leader>b :CmusNext<cr>
```

---
there is another sister project
[`cmus-osx`](https://github.com/azadkuh/cmus-osx) who integrates *cmus* into
`MacOS` notification menu and captures **Fn** music keys.


# License
MIT license - see [license](./LICENSE) for more details.

