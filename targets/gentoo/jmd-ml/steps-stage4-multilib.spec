[section steps/jmd-ml]

stage4-multilib: [

cp /usr/share/zoneinfo/$[jmd-ml/stage4-multilib/timezone] /etc/localtime

eselect profile set default/linux/amd64/10.0/desktop 

layman -S	
layman -a multilib
echo "source /var/lib/layman/make.conf" >> /etc/make.conf

echo 'SETARCH_ARCH_x86="i686"' >> /etc/make.conf
mkdir -p /etc/portage/profile
echo 'app-emulation/wine -scanner -gnutls -nas -dbus -hal -ldap -mp3' >> /etc/portage/profile/package.use.mask

if [ "$[jmd-ml/stage4-multilib/portage/USE?]" = "yes" ]
then
  echo "Addding configuration USE flags"
  euse -E "$[jmd-ml/stage4-multilib/portage/USE:lax]"
fi

emerge abi-wrapper
# The following is to avoid circular references with lib32
FEATURES="-ccache" USE="-ldap -gpm" emerge ncurses
FEATURES="-ccache" USE="-acl" emerge gettext --nodeps

# openssl improperly links if it is already installed
emerge -C openssl
emerge -eN readline

USE="-ldap" emerge dev-libs/cyrus-sasl
emerge openldap openssl

if [ "$[jmd-ml/stage4-multilib/portage/files/package.use?]" = "yes" ]
then
cat >> /etc/portage/package.use << "EOF"
$[[jmd-ml/stage4-multilib/portage/files/package.use:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-multilib/portage/files/package.keywords?]" = "yes" ]
then
cat >> /etc/portage/package.keywords << "EOF"
$[[jmd-ml/stage4-multilib/portage/files/package.keywords:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-multilib/portage/files/package.unmask?]" = "yes" ]
then
cat >> /etc/portage/package.unmask << "EOF"
$[[jmd-ml/stage4-multilib/portage/files/package.unmask:lax]]
EOF
fi
if [ "$[jmd-ml/stage4-multilib/portage/files/package.mask?]" = "yes" ]
then
cat >> /etc/portage/package.mask << "EOF"
$[[jmd-ml/stage4-multilib/portage/files/package.mask:lax]]
EOF
fi

emerge $eopts $[jmd-ml/stage4-multilib/packages] || exit 1
]
