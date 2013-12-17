#the build host
export FASRCSW_BUILD_HOST=hero4502

#the location of production fasrcsw clone
export FASRCSW_PROD=/n/sw/fasrcsw


#---


#check that we're on the build host
if [ -z "${FASRCSW_NO_BUILD_HOST_CHECK:-}" ] && [ "$(hostname -s)" != "$FASRCSW_BUILD_HOST" ]; then
	echo "*** ERROR *** you are not logged into the build host, $FASRCSW_BUILD_HOST" >&2
	return 1
fi

#set the location of this clone
if [ -z "$BASH_SOURCE" ]; then
	echo "*** ERROR *** your bash is too old -- there's no BASH_SOURCE in the environment" >&2
	return 1
fi
export FASRCSW_DEV="$(dirname "$(readlink -e "$BASH_SOURCE")")"  #(the abs path of the dir containing this setup.sh)

