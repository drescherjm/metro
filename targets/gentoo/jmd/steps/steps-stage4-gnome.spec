[section steps/jmd]

stage4-gnome: [
	
	cd /usr/local/gentoo-keywords
	git checkout gnome
	
	options = ${eopts} --newuse --deep --keep-going=y 

	emerge ${options} system || emerge ${options} system || emerge ${options} system || emerge ${options} system
	emerge ${options} world || emerge ${options} world || emerge ${options} world || emerge ${options} world
	emerge ${options} gnome-base/gnome || emerge ${options} gnome-base/gnome || exit 1
	emerge $eopts $[jmd/stage4-gnome/packages:zap] || exit 1

]


