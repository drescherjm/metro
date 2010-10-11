[collect ./stage/common.spec]
[collect ./stage/capture/tar.spec]
[collect ./stage/stage3-generator.spec]

[section path/mirror]

source: $[:source/subpath]/$[source/name].tar.*

[section source]

: stage2
name: $[]-$[:subarch]-$[:version]
version: $[target/version]
subarch: $[target/subarch]
build: $[target/build]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]

# use python2 if available - if not available, assume we are OK with python3
a=$(eselect python list | sed -n -e '1d' -e 's/^.* \(python[23]\..\).*$/\1/g' -e '/python2/p')
# if python2 is available, "$a" should be set to something like "python2.6":
if [ "$a" != "" ]
then
	eselect python set $a
fi

USE="build" emerge --oneshot --nodeps portage || exit 1
export USE="$[portage/USE] bindist lib32"

echo "Emerging Shadow"
emerge --oneshot -k shadow || exit 1

echo "Emerging layman"
emerge $eopts git layman -k || exit 1

layman -S
layman -a multilib
echo "source /var/lib/layman/make.conf" >> /etc/make.conf

echo 'SETARCH_ARCH_x86="i686"' >> /etc/make.conf
mkdir -p /etc/portage/profile
echo 'app-emulation/wine -scanner -gnutls -nas -dbus -hal -ldap -mp3' >> /etc/portage/profile/package.use.mask

echo "Emerging ncurses"
FEATURES="-ccache" USE="-ldap -gpm lib32" emerge $eopts ncurses || exit 1
FEATURES="-ccache" emerge $eopts gpm --nodeps || exit 1
#FEATURES="-ccache" USE="-ldap" emerge ncurses || exit 1

echo "Emerging gettext"
FEATURES="-ccache" USE="-acl lib32" emerge $eopts gettext --nodeps || exit 1
FEATURES="-ccache" emerge $eopts acl || exit 1

echo "Emerging glibc"
emerge $eopts glibc || exit 1

#echo "Emerge gpm"
#FEATURES="-ccache" emerge $eopts  gpm || exit 1

echo "Emerging the system set"
emerge $eopts -e system --keep-going || emerge $eopts -e system --keep-going || emerge $eopts -e system --keep-going || exit 1

# zap the world file and emerge packages
rm -f /var/lib/portage/world || exit 2
if [ "$[emerge/packages?]" = "yes" ]
then
	emerge $eopts $[emerge/packages:lax] || exit 1
fi

# add default runlevel services
if [ "$[baselayout/services?]" = "yes" ]
then
	for service in $[baselayout/services:lax]
	do
		rc-update add $service default
	done
fi

if [ "$[metro/build]" = "funtoo" ] || [ "$[metro/build]" = "~funtoo" ]
then
	eselect vi set busybox
fi
]

euse -E lib32

[section portage]

ROOT: /
