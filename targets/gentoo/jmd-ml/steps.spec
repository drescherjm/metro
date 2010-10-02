[collect ./files.spec]
[collect ./steps-stage4.spec]
[collect ./steps-stage4-desktop.spec]
[collect ./steps-stage4-desktop-multilib.spec]

[section steps/jmd-ml]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[jmd-ml/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[jmd-ml/files/resolv.conf]]
EOF
]

