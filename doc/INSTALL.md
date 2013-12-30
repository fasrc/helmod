# Install fasrcw

<!--
If you're setting this up for an organation other than Harvard FAS Research Computing (github fasrc), create a new canonical fasrcsw remote and adjust urls below accordingly.
-->


## Setup the production repo clone

As root, pick the central location for all cluster software and clone the fasrcsw repo there:
	
	git clone https://github.com/fasrc/fasrcsw.git
	cd fasrcsw

This top level directory will contain everything relevant to the fasrcsw software management system, but actual rpm files, app installations, and other build outputs are .gitignore'd.
Thus, *make sure this is backed up regularly*.

Change to that directory and source the setup.sh:
	
	source ./setup.sh

This makes available some scripts such as `fasrcsw-rpm` and `fasrcsw-rpmbuild-*` which are very thin wrappers around the default programs and just add some default options.
Use the rpm one to initialize the rpm database used exclusively for fasrcsw:

	fasrcsw-rpm --initdb

This repo clone is know as `$FASRCSW_PROD`.
<!--
This clone only needs to pull updates, thus an https remote is fine.
-->


## Have each contributor setup a development repo clone

Clone the repo in some personal location, preferably on network storage, e.g. somewhere in your home directory:

	git clone git@github.com:/fasrc/fasrcsw.git
	cd fasrcsw

Customize `setup.sh`.
In particular, set `FASRCSW_PROD` to point to the location of the production repo above.

These repo clones are know as `$FASRCSW_DEV` (one for each contributor).
<!--
These clones will need to push updates back to the remote.
-->


# Install lmod

Install [lmod](http://www.tacc.utexas.edu/tacc-projects/lmod).
FAS RC uses the [github version](https://github.com/TACC/Lmod).
Point it at the various locations within fasrcsw:

	./configure --prefix="$FASRCSW_PROD"/apps --with-module-root-path="$FASRCSW_PROD"/modulefiles --with-spiderCacheDir="$FASRCSW_PROD"/moduledata/cacheDir --with-updateSystemFn="$FASRCSW_PROD"/moduledata/system.txt


# Install standard compiler and MPI stacks

## gcc

### gmp

### mpfr

### mpc

### gcc
