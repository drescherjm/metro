[section steps/jmd]

stage4-kde: [

	function retry_emerge() {
		emerge ${options} $@ ||  emerge ${options} $@  ||  emerge ${options} $@ ||  emerge ${options} $@ ||  emerge ${options} $@
	}

	pushd .

	layman -L
	layman -a kde
	echo "source /var/lib/layman/make.conf" >> /etc/make.conf
	
	cd /usr/local/gentoo-keywords
	git checkout kde

	cd /etc/portage
	ln -s /usr/local/gentoo-keywords/sets
	popd 
	
	options = ${eopts} --newuse --deep --keep-going=y 

	emerge ${options} system || emerge ${options} system || emerge ${options} system || emerge ${options} system
	
	echo "Updating world"
	retry_emerge world

	echo "Updating qt-core"
	retry_emerge qt-core


	retry_emerge @kdelibs-4.6
	retry_emerge @kde-4.6	

	emerge ${options} @kde-4.6 || emerge ${options} @kde-4.6 || exit 1
	emerge $eopts $[jmd/stage4-kde/packages:zap] || exit 1

]


