[collect ./stage/common.spec]
[collect ./stage/capture/tar.spec]
[collect ./stage/stage3-derivative.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.$[target/compression]

[section target]

name: stage4-$[target/subarch]-$[target/version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
export USE="$[portage/USE] bindist"
emerge $eopts $[emerge/packages/stage4:zap] || exit 1
]

[section portage]

ROOT: /

[section trigger]

ok/run: [
#!/bin/bash

# We completed a successful stage4 build, so record the version of this build in our
# .control/version/stage4 file so that other builds can see that this new version is
# available.

install -d $[path/mirror/control]/version || exit 1
echo "$[target/version]" > $[path/mirror/control]/version/stage4 || exit 1
]
