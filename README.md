# Syncthing module for polybar

This whole script was written some time ago as a proof of concept and is not fully engineered.
But it worked more or less reliably for me since then.
Therefore I'm publishing it if someone is interested in contributing or using.

![idle](img/cropped/idle.png)
![sync](img/cropped/sync.png)
![pause](img/cropped/pause.png)

idle, sync, pause

## Polybar

``` ini
[module/syncthing]
type = custom/script

exec = polybar-syncthing 2>/dev/null
exec-if = pgrep -x syncthing
tail = true

click-left = syncthingctl resume --all-dirs
click-right = syncthingctl pause --all-dirs
click-middle = syncthingctl rescan-all
```

Note that syncthingctl from [syncthingtray](https://github.com/Martchus/syncthingtray) is needed for on-click actions.
You might also need to include the `Font Awesome 6 Free` font in your polybar config. I have it specified as third font in my `config.ini`:
``` ini
font-3 = "Font Awesome 6 Free Solid:pixelsize=10;2"``
```
It is included in the [ttf-font-awesome](https://archlinux.org/packages/community/any/ttf-font-awesome/) package on Arch Linux.
Feel free to replace the used icons and submit PRs for replacing those via command line argument.

## Installation of the script

- make sure that `$HOME/.local/bin` is in your `$PATH`
- then `make install` or just deploy the script to some dir in your `$PATH`

## Similar projects

- [syncthing-status](https://github.com/carldelfin/syncthing-status) written in R lang.

## Todos

- use db.completion endpoint when finally fixed
- show sync conflict with another icon
- fix sometimes hangs on big sync (?)
