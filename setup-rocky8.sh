#--- basic config -- adjust as needed

#the location of production fasrcsw clone
test -z "$FASRCSW_PROD" && export FASRCSW_PROD=/n/sw/helmod-rocky8
test -z "$LMOD_PREFIX" && export LMOD_PREFIX=${FASRCSW_PROD}/apps/lmod

#default compilers and mpi stacks
#update these as versions increase.
#this assumes each FASRCSW_MPIS has been built with each FASRCSW_COMPS
#export FASRCSW_COMPS="gcc/9.5.0-fasrc01"
#export FASRCSW_MPIS="openmpi/4.1.0-fasrc01"

export FASRCSW_COMPS="intel/24.2.1-fasrc01"
export FASRCSW_MPIS="intelmpi/2021.13-fasrc01"

#the build host
export FASRCSW_BUILD_HOST_01=builds01
if [ "$(hostname -s)" != "$FASRCSW_BUILD_HOST_01" ] && [ "$(hostname -s)" != "$FASRCSW_BUILD_HOST_02" ]; then 
	echo "WARNING: the current host is not the canonical build host for Rocky 8, use builds01." >&2
fi

#rpm packager credits
export FASRCSW_AUTHOR="$(getent passwd $USER | cut -d: -f5), Harvard FAS Research Computing <rchelp@fas.harvard.edu>"


#--- environment setup

#set the location of this clone
if [ -z "$BASH_SOURCE" ]; then
	echo "*** ERROR *** your bash is too old -- there's no BASH_SOURCE in the environment" >&2
	return 1
fi
export FASRCSW_DEV="$(dirname "$(readlink -e "$BASH_SOURCE")")"  #(the abs path of the dir containing this setup.sh)

export PATH="$FASRCSW_DEV/bin:$PATH"

#create build directories

if [ ! -d "$FASRCSW_DEV"/rpmbuild/BUILD ]; then
    mkdir "$FASRCSW_DEV"/rpmbuild/BUILD
fi


if [ ! -d "$FASRCSW_DEV"/appdata ]; then
    mkdir "$FASRCSW_DEV"/appdata
fi
