[section steps/jmd]

stage4-gnome: [
	
	cd /usr/local/gentoo-keywords
	git checkout gnome
	
	options="${eopts} --newuse --deep --keep-going=y --autounmask-write"

	emerge ${options} system || emerge ${options} system || emerge ${options} system || emerge -uDvNB system
	emerge ${options} world || emerge ${options} world || emerge ${options} world || emerge -uDvNB world
	emerge ${options} gnome-base/gnome || emerge ${options} gnome-base/gnome || emerge -uDvBN || exit 1
	emerge $eopts $[jmd/stage4-gnome/packages:zap] || emerge -uDvNB $[jmd/stage4-gnome/packages:zap] || exit 1

]


