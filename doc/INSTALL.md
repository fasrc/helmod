# Overview

Most of this is a one-time operation, done by the person setting up fasrcsw.
In order to join an existing fasrcsw environment, [this section](#have-each-contributor-setup-a-development-repo-clone) is all that's needed.

The fasrcsw system is designed to work on a CentOS 6 cluster.
If you're setting this up for an organization other than Harvard FAS Research Computing (@fasrc on github), create a new canonical fasrcsw master remote and adjust urls below accordingly.



# Install fasrcw

## Setup the production repo clone

As root, pick the central location on network storage for all cluster software, and clone the fasrcsw repo there:

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

and set `FASRCSW_PROD` to the absolute path of this fasrcsw clone you just made.
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

Each app contributor should clone the fasrcsw repo in some personal location, preferably on network storage, e.g. somewhere in his or her home directory:

``` bash
git clone git@github.com:/fasrc/fasrcsw.git
cd fasrcsw
```

These clones will need to regularly push updates back to the remote.

Customize `setup.sh` if necessary.
In particular, make sure `FASRCSW_PROD` points to the location of the production repo above.
Assuming someone else has done all the initial setup, you can proceed to the [HOWTO](HOWTO.md).

These repo clones are know as `$FASRCSW_DEV` (one for each contributor).



# Install lmod

The fasrcsw system uses [lmod](http://www.tacc.utexas.edu/tacc-projects/lmod).
<!--
FASRC uses the [github version](https://github.com/TACC/Lmod) of the source code (we encountered trouble building the version on sourceforge).
In particular, these instructions are matched to lmod 5.2, commit c00912cda9.
-->
FASRC uses [the version posted on sourceforge](http://sourceforge.net/projects/lmod/); in particular, these instructions are matched to lmod 5.4.1.

Lmod installation will write files outside of the given `--prefix`, specifically to the root-owned location `/usr/share/zsh/site-functions`.
Rather than running `make install` as root, the following temporarily changes file attributes to allow your regular account's group to write there.
The same approach is taken to just let it write to places within `$FASRCSW_PROD`.

Thus, *this writes to production locations*!
If you're upgrading, the lmod `make install` will automatically update to the `lmod -> X.Y.Z` symbolic link!
(A better procedure for a more controlled upgraded needs to be implemented.)


## Prerequisites and prep

lmod requires `lua` 5.1 or 5.2, plus `lua-filesystem`, `lua-posix`, and `lua-devel` (at least as of lmod version 5.2).

Source a configured fasrcsw clone, or at least define `FASRCSW_PROD` to point to the parent of the production `apps` directory.

Temporarily allow the writes that lmod wants to do (assuming your primary group is a trusted admin group):

``` bash
sudo chgrp $(id -gn) /usr/share/zsh/site-functions
sudo chmod g+w       /usr/share/zsh/site-functions
for f in _ml _module; do
    if [ -f /usr/share/zsh/site-functions/"$f"  ]; then
        sudo chgrp $(id -gn) /usr/share/zsh/site-functions/"$f"
        sudo chmod g+w       /usr/share/zsh/site-functions/"$f"
    fi
done
```

Also, temporarily allow writes to the production apps space:

``` bash
sudo chgrp $(id -gn) "$FASRCSW_PROD"/apps
sudo chmod g+w       "$FASRCSW_PROD"/apps
if [ -d "$FASRCSW_PROD"/apps/lmod/ ]; then
    sudo chgrp $(id -gn) "$FASRCSW_PROD"/apps/lmod
    sudo chmod g+w       "$FASRCSW_PROD"/apps/lmod
fi

```


## If upgrading...

Stop your deployment system from replacing these files before their updates are captured:

``` bash
/usr/share/zsh/site-functions/_ml
/usr/share/zsh/site-functions/_module
```


## Build and install it

Get the source code (stash a copy in `$FASRCSW_PROD/rpmbuild/SOURCES/` for good measure), configure it to use the various locations within fasrcsw, and build it.

``` bash
./configure --prefix="$FASRCSW_PROD"/apps --with-module-root-path="$FASRCSW_PROD"/modulefiles --with-spiderCacheDir="$FASRCSW_PROD"/moduledata/cacheDir --with-updateSystemFn="$FASRCSW_PROD"/moduledata/system.txt
make pre-install
make install
```


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

``` csh
#setenv MODULEPATH `.../apps/lmod/lmod/libexec/addto --append MODULEPATH .../apps/lmod/lmod/modulefiles/Core`
```

And we remove `MODULEPATH $MODULEPATH_ROOT/$LMOD_sys` from the line above that, too.


## Undo the permissions hacks above

Set the zsh directory back to the way it was:

``` bash
sudo chgrp root /usr/share/zsh/site-functions
sudo chmod g-w /usr/share/zsh/site-functions
for f in _ml _module; do
    if [ -f /usr/share/zsh/site-functions/"$f"  ]; then
        sudo chgrp root /usr/share/zsh/site-functions/"$f"
        sudo chmod g-w  /usr/share/zsh/site-functions/"$f"
    fi
done
```

and likewise for the lmod installation location:

``` bash
sudo chgrp root "$FASRCSW_PROD"/apps
sudo chmod g-w "$FASRCSW_PROD"/apps
if [ -d "$FASRCSW_PROD"/apps/lmod/ ]; then
    sudo chgrp root "$FASRCSW_PROD"/apps/lmod
    sudo chmod g-w  "$FASRCSW_PROD"/apps/lmod
fi
```

You may also want to change the ownership of the newly installed lmod version directory and symlink to root, e.g. with something like:

```
VERSION=5.4.1
sudo chown -R root:root "$FASRCSW_PROD"/apps/{lmod,$VERSION}
```


## Other lmod features 

### Spider cache

lmod features optional caching of the modulefile hierarchy to make spider and avail faster; fasrcsw enables this.
Updates of the cache happen during the fasrcsw app build process, therefore no cron job or other automatic update mechanism is necessary.

### Module usage logging

fasrcsw includes a hook for logging module load events to a MySQL database.
To use this, create a MySQL database using [$FASRCSW_PROD/modulehook/modulestats.sql](../modulehook/modulestats.sql), and create a file `$FASRCSW_PROD/modulehook/.my.cnf.modulelogger` with the host, database name, and credentials for connecting to it.
Finally, tell lmod to use this hook by adding the following to `lmod.sh` and `lmod.csh`, respectively, filling in the value of FASRCSW_PROD:

``` bash
export FASRCSW_PROD=...FIXME...
export LMOD_PACKAGE_PATH="$FASRCSW_PROD"/modulehook
```

``` csh
setenv FASRCSW_PROD ...FIXME...
setenv LMOD_PACKAGE_PATH "$FASRCSW_PROD"/modulehook
```

This is the internal lmod/lua logging, which is after resolution of default versions and includes all modules loaded as dependencies.
To go to the extreme and also log what users are asking for on the command line, you can run this patch for `init/bash` and `init/csh` (it assumes `FASRCSW_PROD` is set in the base `lmod.sh` and `lmod.csh` setup scripts as done above):

``` bash
sudo patch --directory="$FASRCSW_PROD"/apps/lmod/lmod -p1 < "$FASRCSW_PROD"/misc/modulelogger.patch
```

(The patch was made against lmod 5.2 but still works in 5.4.1 since there are only minor offsets.)



# Install standard compiler and MPI apps and configure setup.sh to use them

You'll have to build the standard compiler and MPI apps against which all the other apps are built.
Spec files are provided in `rpmbuild/SPECS`, but many of these require hacks that are not yet documented.

Once you've settled upon the sets of compiler and MPI implementations against which to build software by default, set the `FASRCSW_COMPS` and `FASRCSW_MPIS` arrays in `setup.sh` and push these back to the master remote.
