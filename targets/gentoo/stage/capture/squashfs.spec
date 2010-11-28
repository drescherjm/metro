[section steps]

capture: [
#!/bin/bash
outdir=`dirname $[path/mirror/target]`
if [ ! -d $outdir ]
then
	install -d $outdir || exit 1
fi
squashout="$[path/mirror/target]"
squashout="${squashout%.*}.squashfs"
mksquashfs $[path/chroot/stage] $squashout -noappend
if [ $? -ge 2 ]
then
	rm -f "$squashout" "$[path/mirror/target]"
	exit 1
fi
if [ $? -ne 0 ]
then
	echo "Compression error - aborting."
	rm -f $[path/mirror/target]
	exit 99
fi

workdir=$(mktemp -d)
cd $workdir

# While the work should be done in a tmpdir, I could leave all the results
# in the target output dir...
## workdir=$outdir

mkdir -p $workdir/isolinux

# XXX: These tests should go earlier.
if test -f "$[iso/binfile:lax]"; then
	cp "$[iso/binfile]" "$workdir/isolinux"
else
	echo "No ISO 9660 boot code data found - aborting"
	exit 1 # XXX: change exit code to be less generic
fi

cp "$squashout" "$workdir/image.squashfs"
test -d "squashfs-root" && rm -fr "squashfs-root"
unsquashfs $workdir/image.squashfs boot/*

## If this matches more than one, error out.
cp -T squashfs-root/boot/kernel* $workdir/isolinux/kernel || exit 1
cp -T squashfs-root/boot/initramfs* $workdir/isolinux/initramfs || exit 1
cp -T squashfs-root/boot/System.map* $workdir/isolinux/System.map
rm -fr squashfs-root

touch $workdir/livecd

if test "$[iso/files/isolinux.cfg?]" = "yes"; then
	cat >$workdir/isolinux/isolinux.cfg << "EOF"
$[[iso/files/isolinux.cfg]]
EOF
fi

if test "$[iso/files/cdupdate.sh?]" = "yes"; then
	cat >$workdir/cdupdate.sh << "EOF"
$[[iso/files/cdupdate.sh:lax]]
EOF
fi

if test "$[iso/memtest?]" = "yes" && test -f "$[iso/memtest:lax]"; then
	cp "$[iso/memtest]" "$workdir/isolinux/$(basename "$[iso/memtest]")"
	cat <<EOF >>$workdir/isolinux/isolinux.cfg

label memtest
kernel $(basename "$[iso/memtest]")
EOF
fi

for f in $[iso/files/extra:lax]; do
	if test -f "$f"; then
		cp "$f" "$workdir/"
	elif test -d "$f"; then
		cp -r "$f" "$workdir/"
	fi
done

#volid="-V ${squashout%%.squashfs}" # This hack beats all hacks
mkisofs -l -o $[path/mirror/target] \
	-b isolinux/$(basename "$[iso/binfile]") \
	-c isolinux/boot.cat -no-emul-boot -boot-load-size 4 \
	-boot-info-table \
		$workdir/ || exit 1

test "$[iso/hybrid:zap]" = "yes" && isohybrid $[path/mirror/target]

cd - # Return to normal (doesn't really matter unless it does)

if test "$[iso/gpgkey?]" = "yes"; then
	gpg --detach-sign --armor --local-user "$[iso/gpgkey:zap]" \
		$[path/mirror/target] && \
	gpg --verify $[path/mirror/target].asc $[path/mirror/target]
fi

]

