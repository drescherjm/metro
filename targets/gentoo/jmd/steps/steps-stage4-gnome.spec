stage4-gnome: [
	
	cd /usr/local/gentoo-keywords
	git checkout gnome

	emerge $eopts gnome-base/gnome || exit 1
	emerge $eopts $[jmd/stage4-gnome/packages:zap] || exit 1

]


