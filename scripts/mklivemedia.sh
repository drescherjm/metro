#!/bin/sh
# Copyright 2010 Daniel Cordero
# Licensed under the GPLv2

# R e q u i r e m e n t s
#  sys-boot/syslinux (for isolinux.bin)
#  app-cdr/cdrtools
#  sys-fs/squashfs-tools
# a stage5 squashfs from metro

usage() {
	echo -e "$0 [out: <output file>] [bin: <isolinux binary>] \\"
	echo -e "\t\t[cd: <cd directory root>] [hybrid: <yes/no>] \\"
	echo -e "\t\t[mem: <memtest>] [sqfs: ] <squashfs image> \\"
	echo -e "\t\t[sign: <gpg key>] \\"
	echo -e "\t\t[<extra files or directories>...]"
	echo
	echo "Create bootable live media for experimenting with or installing"
	echo "Funtoo Linux."
	echo
	# Remember: Square brackets mean optional; sharp brackets mean
	#	required arguments. Elipsis means they can be repeated.
}

binfile=/usr/share/syslinux/isolinux.bin
cdroot=cd_root

while test "$#" -gt 0; do
	# This could get really ugly.
	# Hopefully you read this message and the following code.
	case "$1" in
	-h)   usage; exit 0;;
	bin:) shift; binfile=$1;;
	cd:)  shift;  cdroot=$1;;
	hybrid:)shift; hybri=$1;;
	mem:) shift; memfile=$1;;
	out:) shift; outfile=$1;;
	sign:) shift; gpgkey=$1;;
	sqfs:) shift;   sqfs=$1;;
	*)	if test "$sqfs"; then
			flist="$flist $1"
		else
			sqfs=$1
		fi;;
	esac
	shift
done

if test x"$sqfs" = "x"; then
	usage
	echo "Squashfs image required - aborting" >&2
	exit 1
fi

test -d "$cdroot" || mkdir $cdroot
test -d "$cdroot/isolinux" || mkdir -p $cdroot/isolinux

if test -f "$binfile"; then
	cp "$binfile" $cdroot/isolinux/
elif test -f $cdroot/isolinux/$(basename ${binfile:-isolinux.bin}); then
	: # pass
else
	usage
	echo "ISOLINUX required - aborting" >&2
	echo "  (set with 'bin: /path/to/isolinux.bin')" >&2
	exit 1
fi

if test -f "$sqfs"; then
	cp "$sqfs" $cdroot/image.squashfs
	test -d "squashfs-root" && rm -fr "squashfs-root"
	unsquashfs $cdroot/image.squashfs boot/*

	## Bug: if this matches more than one.
	cp squashfs-root/boot/kernel* $cdroot/isolinux/kernel
	cp squashfs-root/boot/initramfs* $cdroot/isolinux/initramfs
	cp squashfs-root/boot/System.map* $cdroot/isolinux/System.map
	rm -fr squashfs-root
else
	usage
	echo "Squashfs image required - aborting" >&2
	exit 1
fi

for f in $flist; do
	if test -f "$f"; then
		cp "$f" "$cdroot"
	elif test -d "$f"; then
		cp -r "$f" "$cdroot"
	fi
done

touch $cdroot/livecd
cat << EOF >$cdroot/isolinux/isolinux.cfg
prompt 1
default funtoo

label funtoo
  kernel kernel
  append root=/dev/ram0 looptype=squashfs loop=/image.squashfs cdroot
  initrd initramfs
EOF

if test "$memfile" && test -f "$memfile"; then
	cp "$memfile" $cdroot/isolinux/$(basename "$memfile")
	cat <<EOF >>$cdroot/isolinux/isolinux.cfg

label memtest
  kernel $(basename "$memfile")
EOF
fi

cat >$cdroot/cdupdate.sh <<'EOF'
#!/bin/sh
# This is not very robust. Sorry.

. /etc/initrd.defaults

(test -d $NEW_ROOT/libexec/rc/init.d || mkdir -p $NEW_ROOT/libexec/rc/init.d) \
	|| exit 1

cp -ar $NEW_ROOT/mnt/livecd/libexec/rc $NEW_ROOT/libexec || exit 1
#mount -t tmpfs -o nosuid,nodev,noexec,relatime,size=1024k,mode=755 \
#	tmpfs $NEW_ROOT/libexec/rc/init.d || exit 1
EOF

test "$outfile" && volid="-V ${outfile%%.iso}" # BUG: spaces in name
mkisofs -l -o ${outfile:-funtoo.iso} \
	-b isolinux/$(basename ${binfile:-isolinux.bin}) \
	-c isolinux/boot.cat -no-emul-boot -boot-load-size 4 \
	-boot-info-table $volid \
		$cdroot/

test x"${hybri:-no}" = "xyes" && isohybrid ${outfile:-funtoo.iso}

if test x"$gpgkey" != "x"; then
	gpg --detach-sign --armor --local-user "$gpgkey" ${outfile:-funtoo.iso}
	gpg --verify ${outfile:-funtoo.iso}.asc ${outfile:-funtoo.iso}
fi
