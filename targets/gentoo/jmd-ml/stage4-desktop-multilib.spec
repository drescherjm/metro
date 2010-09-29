[collect ../stage/common.spec]
[collect ../stage/capture/tar.spec]
[collect ../stage/stage3-derivative.spec]
[collect ../stage/symlink.spec]
[collect ./steps.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]

name: stage4-desktop-multilib-$[target/subarch]-$[target/version]
name/current: stage4-desktop-multilib-$[target/subarch]-current

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
$[[steps/jmd-ml-ml/setup]]

export USE="$[portage/USE] bindist"
$[[steps/jmd-ml-ml/stage4-desktop-multilib]]
]

[section trigger]

ok/run: [
$[[trigger/ok/symlink]]
]

[section portage]

ROOT: /
