[section steps/jmd-ml]

stage4-desktop: [

#euse -E kde gnome X 

eselect profile set default/linux/amd64/10.0/desktop 

USE="-ldap" emerge dev-libs/cyrus-sasl
emerge openldap

if [ "$[jmd-ml/stage4-desktop/portage/USE?]" = "yes" ]
then
  echo "Addding configuration USE flags"
  euse -E "$[jmd-ml/stage4-desktop/portage/USE:lax]"
fi

if [ "$[jmd-ml/stage4-desktop/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[jmd-ml/stage4-desktop/portage/files/package.use:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[jmd-ml/stage4-desktop/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[jmd-ml/stage4-desktop/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[jmd-ml/stage4-desktop/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts $[jmd-ml/stage4-desktop/packages] || exit 1
]

