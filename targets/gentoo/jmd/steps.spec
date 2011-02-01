[collect ./files.spec]
[collect ./steps/steps-stage4.spec]
[collect ./steps/steps-stage4-gnome.spec]

[section steps/jmd]

setup: [
# the quotes below prevent variable expansion of anything inside make.conf
cat << "EOF" > /etc/make.conf
$[[jmd/files/make.conf]]
EOF
cat << "EOF" > /etc/resolv.conf
$[[jmd/files/resolv.conf]]
EOF

echo "SETUP SETUP SETUP"
]
