#!/bin/bash

# If we are running from fcron, we'll have a clean environment and thus won't
# have proxy settings. So let's make sure we have a good Gentoo environment...

source /etc/profile

die() {
	echo $*
	exit 1
}

do_help() {
	cat << EOF

  Metro Automation Engine Script
  by Daniel Robbins (drobbins@funtoo.org)
  by Benedikt Böhm (hollow@gentoo.org)

  Usage: $0 <build> <arch>..
  Examples:
    # $0 hollow amd64 i686
    # $0 ~funtoo core2

EOF
}

if [ "$METRO" = "" ]
then
	METRO=$(which metro)
fi

if [ ! -e $METRO ]
then
	die "Metro is required for build.sh to run"
fi

if [ $# -lt 2 ]
then
	do_help
	die "This script requires two or more arguments"
fi

VERS=`date +%Y%m%d`
BUILD="$1"
shift

for SUBARCH in "$@"
do
	nice -n 39 ionice -c 3 $METRO multi: yes metro/build: $BUILD target/subarch: $SUBARCH target/version: $VERS multi/mode: freshen
done
