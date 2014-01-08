# Overview

The fasrcsw system is designed to work on a CentOS 6 cluster.

If you're setting this up for an organization other than Harvard FAS Research Computing (@fasrc on github), create a new canonical fasrcsw master remote and adjust urls below accordingly.



# Install fasrcw

## Setup the production repo clone

As root, pick the central location on network storage for all cluster software and clone the fasrcsw repo there:

``` bash
git clone git@github.com:/fasrc/fasrcsw.git
cd fasrcsw
```

Aside from initial configuration, this clone only needs to pull updates, so changing to an https remote later is fine.

This top-level directory will contain everything relevant to the fasrcsw software management system, but actual rpm files, app installations, and other build outputs are .gitignore'd.
Thus, *make sure this is backed up regularly*.

Edit the configuration:

``` bash
$EDITOR setup.sh
```

and set `FASRCSW_PROD` the the absolute path of this fasrcsw clone you just made.
Push these changes back to the remote.

Source the setup.sh:

``` bash
source ./setup.sh
```

This makes available some scripts such as `fasrcsw-rpm` and `fasrcsw-rpmbuild-*` which are very thin wrappers around the normal programs and just add some default options.
Use the rpm one to initialize the rpm database used exclusively for fasrcsw:

``` bash
fasrcsw-rpm --initdb
```

This repo clone is the one and only `$FASRCSW_PROD`.


## Have each contributor setup a development repo clone

Each contributor should clone the fasrcsw repo in some personal location, preferably on network storage, e.g. somewhere in his or her home directory:

``` bash
git clone git@github.com:/fasrc/fasrcsw.git
cd fasrcsw
```

These clones will need to regularly push updates back to the remote.

Customize `setup.sh` if necessary.
In particular, make sure `FASRCSW_PROD` points to the location of the production repo above.

These repo clones are know as `$FASRCSW_DEV` (one for each contributor).



# Install lmod

The fasrcsw system uses [lmod](http://www.tacc.utexas.edu/tacc-projects/lmod).
FAS RC uses the [github version](https://github.com/TACC/Lmod) of the source code (we encountered trouble building the version on sourceforge).


## Prerequisites

lmod requires `lua` 5.1 or 5.2, plus `lua-filesystem`, `lua-posix`, and `lua-devel`.


<!--
## Hack around lmod's ignoring of prefix for some files

During the installation, lmod will try to write files to the main filesystem.
Allow this temporarily:

``` bash
sudo chgrp $(id -gn) /usr/share/zsh/site-functions
sudo chmod g+w /usr/share/zsh/site-functions
```
-->


## Build and install it

Source a configured fasrcsw clone, or at least define `FASRCSW_PROD` to point to the production `apps` dir.


Get the source code, configure it to use the various locations within fasrcsw, and build it.
Since this writes to `$FASRCSW_PROD`, run as root:

``` bash
./configure --prefix="$FASRCSW_PROD"/apps --with-module-root-path="$FASRCSW_PROD"/modulefiles --with-spiderCacheDir="$FASRCSW_PROD"/moduledata/cacheDir --with-updateSystemFn="$FASRCSW_PROD"/moduledata/system.txt
make pre-install
make install
```

*Note that this also installs some files in `/usr/share/zsh/site-functions`!*.
Once done setting up lmod, you may want to remove the following:

```
/usr/share/zsh/site-functions/_ml
/usr/share/zsh/site-functions/_module
```


<!--
## Undo the hack above

Set that directory back to the way it was:

``` bash
sudo chgrp root /usr/share/zsh/site-functions
sudo chmod g-w /usr/share/zsh/site-functions
```
-->


## Distribute configuration to all cluster nodes

By whatever means your cluster uses (e.g. puppet), distribute lmod's configuration files to all cluster nodes:

``` bash
FROM lmod BUILD                               ON ALL HOSTS
--------------------------------------------------------------------
/usr/share/zsh/site-functions/_ml            (same thing)
/usr/share/zsh/site-functions/_module        (same thing)

"$FASRCSW_PROD"/apps/lmod/lmod/init/profile  /etc/profile.d/lmod.sh
"$FASRCSW_PROD"/apps/lmod/lmod/init/cshrc    /etc/profile.d/lmod.csh
```

We also comment out the following lines in `lmod.sh` and `lmod.csh` respectively (where `...` is `$FASRCSW_PROD`), to un-clutter the module namespace:

``` bash
#export MODULEPATH=$(.../apps/lmod/lmod/libexec/addto --append MODULEPATH .../apps/lmod/lmod/modulefiles/Core)
```

``` bash
#setenv MODULEPATH `.../apps/lmod/lmod/libexec/addto --append MODULEPATH .../apps/lmod/lmod/modulefiles/Core`
```



# Install standard compiler and MPI apps and configure setup.sh to use them

You'll have to build the standard compiler and MPI apps that all the other packages are built against.
Spec files are provided in `rpmbuild/SPECS`, but many of these require hacks that are not yet documented.

Once you've settled upon the sets of compiler and MPI implementations against which to build software by default, set the `FASRCSW_COMPS` and `FASRCSW_MPIS` arrays in `setup.sh` and push these back to the master remote.



# Verify

Make sure that `$FASRCSW_PROD` is backed up.
