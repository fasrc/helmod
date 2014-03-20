#!/usr/bin/env bash

# Copyright (c) 2014, Harvard FAS Research Computing
# All rights reserved.

set -e

helpstr="\
NAME
	createSystemCacheFile.sh - update Lmod's spider cache

SYNOPSIS
	createSystemCacheFile.sh --spiderCacheDir DIRECTORY --updateSystemFn PATH

DESCRIPTION
	This is meant to be run as a cron job.

OPTIONS
	--spiderCacheDir DIRECTORY
		Whatever --with-spiderCacheDir Lmod was configured with (the full patch 
		to the cache directory).

	--updateSystemFn PATH
		Whatever --updateSystemFn Lmod was configured with (the full path to 
		the system.txt file).
	
	--lmodSetupScript PATH
		The environment setup for Lmod.  The default is /etc/profile.d/lmod.sh.

	-h, --help
		Print this help.

REQUIREMENTS
	n/a

BUGS/TODO
	n/a

AUTHOR
	Copyright (c) 2014, Harvard FAS Research Computing
	All rights reserved.

	Inspired by TACC's 
	Lmod/contrib/BuildSystemCacheFile/createSystemCacheFile.sh
"

#these are NOT normal Lmod environment variable
#they should exactly match the corresponding --with-* ./configure options
spiderCacheDir=''
updateSystemFn=''
lmodSetupScript=/etc/profile.d/lmod.sh

args=$(getopt -n "$(basename "$0")" -l spiderCacheDir:,updateSystemFn:,help -o h -- "$@")
if [ $? -ne 0 ]; then
	exit 65  #(getopt will have written the error message)
fi
eval set -- "$args"
while [ ! -z "$1" ]; do
	case "$1" in
		--spiderCacheDir)
			spiderCacheDir="$2"
			shift
			;;
		--updateSystemFn)
			updateSystemFn="$2"
			shift
			;;

		-h | --help)
			echo -n "$helpstr"
			exit 0
			;;
		--) 
			shift
			break
			;;
	esac
	shift
done

#make sure options were set
if [ -z "$spiderCacheDir" -o -z "$updateSystemFn" ]; then
	echo "*** ERROR *** both --spiderCacheDir and --updateSystemFn must be specified" >&2
	exit 1
fi

#make sure normal lmod environment is setup
test -e "$lmodSetupScript" && source "$lmodSetupScript"
if [ -z "$LMOD_DIR" -o -z "$MODULEPATH_ROOT" ]; then
	echo "*** ERROR *** basic Lmod environment variables must be set in order for this to work" >&2
	exit 1
fi

set -u


#---

#write the cache file
"$LMOD_DIR"/spider -o moduleT "$MODULEPATH_ROOT" > "$spiderCacheDir"/moduleT.lua.new
test -e "$spiderCacheDir"/moduleT.lua && cp -af "$spiderCacheDir"/moduleT.lua{,.old}
mv "$spiderCacheDir"/moduleT.lua{.new,}

#update the timestamp file
touch "$updateSystemFn"
