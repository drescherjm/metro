[section steps/jmd]

stage4-desktop-multilib: [

eselect profile set default/linux/amd64/10.0/desktop 

layman -S	
layman -a multilib
echo "source /var/lib/layman/make.conf" >> /etc/make.conf

if [ "$[jmd/stage4-desktop-multilib/portage/USE?]" = "yes" ]
then
  echo "Addding configuration USE flags"
  euse -E "$[jmd/stage4-desktop-multilib/portage/USE:lax]"
fi

# openssl improperly links if it is already installed
emerge -C openssl

# The following is to avoid circular references with lib32
USE="-ldap -gpm" emerge ncurses
USE="-acl" emerge gettext

USE="-ldap" emerge dev-libs/cyrus-sasl
emerge openldap

if [ "$[jmd/stage4-desktop-multilib/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[jmd/stage4-desktop-multilib/portage/files/package.use:lax]]
EOF
fi
if [ "$[jmd/stage4-desktop-multilib/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[jmd/stage4-desktop-multilib/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[jmd/stage4-desktop-multilib/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[jmd/stage4-desktop-multilib/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[jmd/stage4-desktop-multilib/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[jmd/stage4-desktop-multilib/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts $[jmd/stage4-desktop-multilib/packages] || exit 1
]
