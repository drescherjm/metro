[collect ./files.spec]
[collect ./steps-stage4-desktop-multilib.spec]

[section steps/jmd-ml]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[jmd-ml/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[jmd-ml/files/resolv.conf]]
EOF
]

stage4: [

if [ "$[jmd-ml/stage4/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[jmd-ml/stage4/portage/files/package.use:lax]]
EOF
fi
if [ "$[jmd-ml/stage4/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[jmd-ml/stage4/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[jmd-ml/stage4/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[jmd-ml/stage4/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[jmd-ml/stage4/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[jmd-ml/stage4/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts -C mail-mta/ssmtp mail-mta/nullmailer || exit 1
rm -f /var/mail
emerge $eopts net-mail/mailbase -1 || exit 1
emerge $eopts mail-mta/postfix || exit 1
emerge $eopts $[jmd-ml/stage4/packages] || exit 1
]

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

