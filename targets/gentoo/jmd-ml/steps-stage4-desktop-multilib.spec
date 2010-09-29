[section steps/jmd-ml]

stage4-desktop-multilib: [

cp /usr/share/zoneinfo/$[jmd-ml/stage4-desktop-multilib/timezone] /etc/localtime

eselect profile set default/linux/amd64/10.0/desktop 

layman -S	
layman -a multilib
echo "source /var/lib/layman/make.conf" >> /etc/make.conf

echo 'SETARCH_ARCH_x86="i686"' >> /etc/make.conf

if [ "$[jmd-ml/stage4-desktop-multilib/portage/USE?]" = "yes" ]
then
  echo "Addding configuration USE flags"
  euse -E "$[jmd-ml/stage4-desktop-multilib/portage/USE:lax]"
fi

# openssl improperly links if it is already installed
emerge -C openssl

emerge abi-wrapper
# The following is to avoid circular references with lib32
USE="-ldap -gpm" emerge ncurses
USE="-acl" emerge gettext

USE="-ldap" emerge dev-libs/cyrus-sasl
emerge openldap

if [ "$[jmd-ml/stage4-desktop-multilib/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[jmd-ml/stage4-desktop-multilib/portage/files/package.use:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop-multilib/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[jmd-ml/stage4-desktop-multilib/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop-multilib/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[jmd-ml/stage4-desktop-multilib/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-desktop-multilib/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[jmd-ml/stage4-desktop-multilib/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts $[jmd-ml/stage4-desktop-multilib/packages] || exit 1
]
