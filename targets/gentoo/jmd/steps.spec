[collect ./files.spec]

[section steps/jmd]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[jmd/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[jmd/files/resolv.conf]]
EOF
]

stage4: [
emerge $eopts -C mail-mta/ssmtp mail-mta/nullmailer || exit 1
rm -f /var/mail
emerge $eopts net-mail/mailbase -1 || exit 1
emerge $eopts mail-mta/postfix || exit 1
emerge $eopts $[jmd/stage4/packages] || exit 1
]

stage4-desktop: [

if [ "$[stage4-desktop/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[stage4-desktop/portage/files/package.use:lax]]
EOF
fi
if [ "$[stage4-desktop/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[stage4-desktop/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[stage4-desktop/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[stage4-desktop/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[stage4-desktop/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[stage4-desktop/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts $[jmd/stage4-desktop/packages] || exit 1
]
