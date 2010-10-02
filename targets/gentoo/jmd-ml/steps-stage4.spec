[section steps/jmd-ml]

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
