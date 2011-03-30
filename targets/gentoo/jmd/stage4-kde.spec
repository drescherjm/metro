[collect ./stage/common.spec]
[collect ./stage/capture/tar.spec]
[collect ./stage/stage3-derivative.spec]
[collect ./stage/symlink.spec]
[collect ./steps.spec]

[section path/mirror]

target: $[:target/subpath]/jmd/$[target/name].tar.xz
#source: $[:source/subpath]/jmd/$[source/name].tar.xz

[section target]

name: stage4-kde-$[target/subarch]-$[target/version]
name/current: stage4-kde-$[target/subarch]-current

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/jmd/setup]]

export USE="$[portage/USE] bindist"
$[[steps/jmd/stage4-kde]]
]

[section trigger]

ok/run: [
$[[trigger/ok/symlink]]
install -d $[path/mirror/control]/version || exit 1
echo "$[target/version]" > $[path/mirror/control]/version/jmd/stage4-kde || exit 1
]

[section portage]

ROOT: /
