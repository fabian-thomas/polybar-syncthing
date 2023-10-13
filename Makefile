install:
	ln -sf "$(realpath polybar-syncthing.py)" "$(HOME)/.local/bin/polybar-syncthing"

crop-images: img/*.png
	convert img/*.png -crop 68x20+1102+0 -set filename:new 'img/cropped/%t' '%[filename:new].png'
