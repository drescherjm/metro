[section target]

arch: amd64

[section portage]

CFLAGS: -march=core2 -msse4 -mcx16 -mpopcnt -msahf -O2 -pipe
CHOST: x86_64-pc-linux-gnu
HOSTUSE: mmx sse sse2
