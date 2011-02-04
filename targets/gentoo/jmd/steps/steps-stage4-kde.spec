[section steps/jmd]

stage4-kde: [
	
	cd /usr/local/gentoo-keywords
	git checkout kde
	
	options = ${eopts} --newuse --deep --keep-going=y 

	emerge ${options} system || emerge ${options} system || emerge ${options} system || emerge ${options} system
	emerge ${options} world || emerge ${options} world || emerge ${options} world || emerge ${options} world
	emerge ${options} @kdelibs-4.6 || emerge ${options} @kdelibs-4.6 || exit 1
	emerge ${options} @kde-4.6 || emerge ${options} @kde-4.6 || exit 1
	emerge $eopts $[jmd/stage4-kde/packages:zap] || exit 1

]


