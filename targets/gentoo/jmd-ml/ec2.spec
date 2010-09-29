[collect ../stage/common.spec]
[collect ../stage/capture/ami.spec]
[collect ./steps.spec]

[section source]

: stage4
name: $[]-$[:subarch]-$[:version]
build: $[target/build]
subarch: $[target/subarch]
version: << $[path/mirror/control]/version/stage3

[section target]

name: gentoo-ec2-$[target/subarch]-$[target/version]

[section path/mirror]

source: $[:source/subpath]/$[source/name].tar.bz2
target: $[:source/subpath]/$[target/name].tar.bz2

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/jmd-ml/setup]]

export USE="$[portage/USE] bindist"

# setup some stuff, so we can run out-of-the-box
env-update && source /etc/profile
cp /usr/share/zoneinfo/$[jmd-ml/ec2/timezone] /etc/localtime

cat << "EOF" > /etc/fstab
$[[jmd-ml/files/ec2/fstab]]
EOF

emerge $eopts net-misc/dhcpcd
rc-update add net.eth0 default

emerge $eopts net-misc/openssh
rc-update add sshd default

emerge $eopts $[jmd-ml/ec2/packages]

for service in $[jmd-ml/ec2/services]; do
	rc-update add ${service} default
done

sed -i -e 's/^# \(%wheel\tALL=(ALL)\tALL\)$/\1/' /etc/sudoers
]

[section portage]

ROOT: /
