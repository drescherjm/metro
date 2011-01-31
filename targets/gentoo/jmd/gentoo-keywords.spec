[section steps]

gentoo_keywords/setup: [

if [ $[portage/gentoo_keywords/source?] == "yes" ]
then
	echo "Setting up package keywords to ${current_root}/usr/local/gentoo-keywords"

        pushd .

	if [ -d ${current_root}/usr/local/gentoo-keywords ];
	then
		cd ${current_root}/usr/local/gentoo-keywords
	   	if [ -e ${current_root}/usr/local/gentoo-keywords/.git ];
	   	then
			git pull
			git fetch
	   	else
			git clone $[portage/gentoo_keywords/source]	
		fi 
	else
		install -d ${current_root}/usr/local	
		cd ${current_root}/usr/local	
		git clone $[portage/gentoo_keywords/source]
		cd gentoo-keywords
	fi

	if [ $[portage/gentoo_keywords/branch?] == "yes" ];
	then
		git checkout $[portage/gentoo_keywords/branch]
	else
		git checkout base
	fi

	git branch

        install -d ${current_root}/etc/portage

        cd ${current_root}/etc/portage

	rm ${current_root}/etc/portage/package.keywords 2> /dev/null
	rm ${current_root}/etc/portage/package.mask	2> /dev/null
	rm ${current_root}/etc/portage/package.unmask	2> /dev/null
	rm ${current_root}/etc/portage/package.use	2> /dev/null

        ln -s ../../usr/local/gentoo-keywords/package.keywords
        ln -s ../../usr/local/gentoo-keywords/package.mask
        ln -s ../../usr/local/gentoo-keywords/package.unmask
        ln -s ../../usr/local/gentoo-keywords/package.use
        popd

fi

]
