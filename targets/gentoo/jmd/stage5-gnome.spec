[collect ./stage/common.spec]
[collect ./stage/capture/squashfs.spec]

[section path/mirror]

source: $[:source/subpath]/$[source/name].tar.*

[section source]
: jmd/stage4-gnome
version: << $[path/mirror/control]/version/$[]
name: $[]-$[:subarch]-$[:version]

build: $[target/build]
subarch: $[target/subarch]


[section path/mirror]

target: $[:source/subpath]/$[target/name].iso

[section target]

name: stage5-$[target/subarch]-$[:version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]

pushd .
cd /usr/local/gentoo-keywords
git checkout gnome
popd

USE=-dynamic emerge $eopts cryptsetup || exit 1

emerge -uDvN gentoo-sources genkernel || exit 1

echo > /etc/fstab || exit 1
if [ -e /var/tmp/cache/genkernel ]; 
then
	genkernel $[jmd/stage5-gnome/genkernel/opts:lax] --cachedir=/var/tmp/cache/genkernel all || exit 1
else
	genkernel $[jmd/stage5-gnome/genkernel/opts:lax] all || exit 1
fi

sed -i -e '/^c/s!agetty 38400!mingetty --autologin root --noclear!' \
	/etc/inittab || exit 1

for i in $[jmd/stage5-gnome/services:zap]; do ln -s /etc/init.d/$i /etc/runlevels/default; done
]

[section portage]

ROOT: /

[section trigger]

ok/run: [
#!/bin/bash

# The stage5.squashfs isn't needed (if it is, take it from the iso:
squashout="$[path/mirror/target]"
rm -f "${squashout%%.*}.squashfs"

]
