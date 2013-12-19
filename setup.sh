#--- basic config -- adjust as needed

#the location of production fasrcsw clone
export FASRCSW_PROD=/n/sw/fasrcsw

#default compilers and mpi stacks
#update these as versions increase.
#this assumes each FASRCSW_MPIS has been built with each FASRCSW_COMPS
FASRCSW_COMPS=(
	gcc/4.8.1-fasrc01
	intel/13.0.079-fasrc01
)
FASRCSW_MPIS=(
	openmpi/1.7.2-fasrc01
	mvapich2/2.0b-fasrc01
)

#the build host
export FASRCSW_BUILD_HOST=hero4502


#--- environment setup

#set the location of this clone
if [ -z "$BASH_SOURCE" ]; then
	echo "*** ERROR *** your bash is too old -- there's no BASH_SOURCE in the environment" >&2
	return 1
fi
export FASRCSW_DEV="$(dirname "$(readlink -e "$BASH_SOURCE")")"  #(the abs path of the dir containing this setup.sh)

export PATH="$FASRCSW_DEV/bin:$PATH"
