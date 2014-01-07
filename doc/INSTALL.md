# Overview

The fasrcsw system is designed to work on a CentOS 6 cluster.



# Install fasrcw

If you're setting this up for an organization other than Harvard FAS Research Computing (github fasrc), create a new canonical fasrcsw remote and adjust urls below accordingly.


## Setup the production repo clone

As root, pick the central location for all cluster software and clone the fasrcsw repo there:

``` bash
git clone https://github.com/fasrc/fasrcsw.git
cd fasrcsw
```

This clone only needs to pull updates, thus an https remote is fine.
This top level directory will contain everything relevant to the fasrcsw software management system, but actual rpm files, app installations, and other build outputs are .gitignore'd.
Thus, *make sure this is backed up regularly*.

Change to that directory and source the setup.sh:

``` bash
source ./setup.sh
```

This makes available some scripts such as `fasrcsw-rpm` and `fasrcsw-rpmbuild-*` which are very thin wrappers around the normal programs and just add some default options.
Use the rpm one to initialize the rpm database used exclusively for fasrcsw:

``` bash
fasrcsw-rpm --initdb
```

This repo clone is know as `$FASRCSW_PROD`.


## Have each contributor setup a development repo clone

Clone the repo in some personal location, preferably on network storage, e.g. somewhere in your home directory:

``` bash
git clone git@github.com:/fasrc/fasrcsw.git
cd fasrcsw
```

These clones will need to push updates back to the remote.

Customize `setup.sh`.
In particular, set `FASRCSW_PROD` to point to the location of the production repo above.

These repo clones are know as `$FASRCSW_DEV` (one for each contributor).



# Install lmod

The fasrcsw system uses [lmod](http://www.tacc.utexas.edu/tacc-projects/lmod).
FAS RC uses the [github version](https://github.com/TACC/Lmod) of the source code (the sourceforge did not build).


## Prerequisites

lmod requires `lua` 5.1 or 5.2, plus `lua-filesystem`, `lua-posix`, and `lua-devel`.


## Hack around lmod's ingorning of --prefix

During the installation, lmod will try to write files to the main filesystem.
Allow this temporarily:

``` bash
	sudo chgrp $(id -gn) /usr/share/zsh/site-functions
	sudo chmod g+w /usr/share/zsh/site-functions
```

Source an configured fasrcsw clone, or at least define `FASRCSW_PROD` to point to the production `apps` dir.


Get the source code, point it at the various locations within fasrcsw, and build it:

``` bash
./configure --prefix="$FASRCSW_PROD"/apps --with-module-root-path="$FASRCSW_PROD"/modulefiles --with-spiderCacheDir="$FASRCSW_PROD"/moduledata/cacheDir --with-updateSystemFn="$FASRCSW_PROD"/moduledata/system.txt
make pre-install
make install
```

## Undo the hack above

Set this directly back to the way it was:

``` bash
sudo chgrp root /usr/share/zsh/site-functions
sudo chmod g-w /usr/share/zsh/site-functions
```

## Distribute configuration to all cluster nodes

By whatever means your cluster uses (e.g. puppet), distribute lmod's supporting files:

``` bash
FROM lmod BUILD                               ON ALL HOSTS
--------------------------------------------------------------------
/usr/share/zsh/site-functions/_ml            (same thing)
/usr/share/zsh/site-functions/_module        (same thing)

"$FASRCSW_PROD"/apps/lmod/lmod/init/profile  /etc/profile.d/lmod.sh
"$FASRCSW_PROD"/apps/lmod/lmod/init/cshrc    /etc/profile.d/lmod.csh
```



# Install standard compiler and MPI stacks

...TODO...
