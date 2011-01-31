[section steps]

gentoo_keywords/setup: [

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
			git clone ${keywords_url}
		fi 
	else
		install -d ${current_root}/usr/local	
		cd ${current_root}/usr/local	
		git clone ${keywords_url}
		cd gentoo-keywords
	fi

	git checkout ${keywords_branch}
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

]
