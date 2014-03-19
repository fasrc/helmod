# How to build and install an app


## Overview

The basic workflow to build an app using fasrcsw is:

* get the source
* create and partially complete a spec file, using the template as a starting point
* do a preliminary build of the software to see what it creates, in order to know what to put in the module file
* complete the spec file and build the final rpm(s)
* install the rpm(s)
* commit changes and move the build outputs to production locations

The default behavior and templates are designed to work with GNU-toolchain-style software packages, i.e. things that use `configure`/`make`/`make install` with standard options, with as little modification as possible.
As an example, this document uses the automake hello-world example, `amhello-1.0.tar.gz`, distributed with automake.


## Prepare

Get ready to build software:

* make sure you've cloned and configured fasrcsw according to [this](INSTALL.md#have-each-contributor-setup-a-development-repo-clone)
* make sure you're logged into the build host
* make sure you're logged into your normal user account, *not* root

`cd` to your personal fasrcsw clone.
Make sure your clone is up-to-date and your environment is pristine, and setup the environment:

``` bash
git pull
module purge
source ./setup.sh
```

There will now be two environment variables defined that are used in the instructions below --
`$FASRCSW_DEV` is the location of your personal clone, and
`$FASRCSW_PROD` is the production one, the central location for your organization's software.

Set these variables particular to the app you're installing:

``` bash
export NAME=...
export VERSION=...
export RELEASE=...
export TYPE=...
```

`NAME` and `VERSION` are whatever the app claims, though some adjustments may be required -- see [this FAQ item](FAQ.md#what-are-the-naming-conventions-and-restrictions-for-an-apps-name-version-and-release).
`RELEASE` is used to track the build under the fasrcsw system and should be of the form `fasrc##` where `##` is a two-digit number.
If this is the first fasrcsw-style build, use `fasrc01`; otherwise increment the fasrc number used in the previous spec file for the app.

Regarding `TYPE`, a major purpose of fasrcsw is to manage entire software environments for multiple compiler and MPI implementations.
Apps are therefore categorized by their *dependencies* (see [this FAQ item](FAQ.md#why-is-a-compiler-a-core-app-and-not-a-comp-app--why-is-an-mpi-implementation-a-comp-app-and-not-an-mpi-app) more about this initially non-intuitive convention, adopted from TACC):

* A *Core* app is one that does not depend on a compiler or MPI implementation.  The compilers themselves, and their dependencies, are core apps, but that's about it.
* A *Comp* app is one that depends upon compiler but not MPI implementation.  The MPI implementation apps themselves are *Comp* apps, as are almost all general, non-mpi-enabled apps.
* A *MPI* app is one that depends upon MPI implementation, and therefore upon compiler, too.

Set `TYPE` to the string `Core`, `Comp`, or `MPI`.

For example, to test the simple *Core* case with `amhello`: `export NAME=amhello ; export VERSION=1.0 ; export RELEASE=$USER ; export TYPE=Core`.
Note that this breaks convention and uses `$USER` for the `RELEASE` instead of `fasrc01` -- this is to avoid people clobbering each other during a demo.
The `amhello` example can be used to test all app types, even though the dependencies are not real.



## Get the source code

By whatever means necessary, get a copy of the app source archive into the location for the sources.
For example:

``` bash
cd "$FASRCSW_DEV"/rpmbuild/SOURCES
wget --no-clobber http://...
```

For `amhello`, which is a bit complicated because it's a tarball within another tarball, see [this FAQ item](FAQ.md#how-do-i-download-amhello-10targz).


## Create a preliminary spec file

Change to the directory of spec files:

``` bash
cd "$FASRCSW_DEV"/rpmbuild/SPECS
```

Create a spec file for the app based upon the template:

``` bash
cp -ai template.spec "$NAME-$VERSION-$RELEASE".spec
```

Now edit the spec file:

``` bash
$EDITOR "$NAME-$VERSION-$RELEASE".spec
```

and address things with the word `FIXME` in them.
For some things, the default will be fine.
Eventually all need to be addressed, but for now, just complete everything up to where `modulefile.lua` is created.
The next step will provide the necessary guidance on what to put in the module file.

If the app you're building requires other apps, follow the templates for loading the appropriate modules during the `%build` step and having the module file require them, too.
See [this FAQ item](FAQ.md#how-are-simple-app-dependencies-handled) for more details.

If you need to add options to the `./configure` command, you can append them to the `%configure` macro.
If the build procedure is very different from a standard `configure`/`make`/`make install`, you'll have to manually code the corresponding steps -- see [this FAQ item](FAQ.md#how-do-i-compile-manually-instead-of-using-the-rpmbuild-macros) for details.
If it's different for different compilers and/or MPI implementations, see [this FAQ item](FAQ.md#how-do-i-use-one-spec-file-to-handle-all-compiler-and-mpi-implementations).



## Do a trial build and inspect its output

The result of the above will be enough of a spec file to basically build the software.
However, you have to build it and examine its output in order to know what to put in the module file that the rpm is also responsible for constructing.
The template spec has a section that, if the macro `trial` is defined, will quit the rpmbuild during the `%install` step and use the `tree` command to dump out what was built and will be installed.

There are also three different scripts depending on the type of app being built -- `fasrcsw-rpmbuild-Core`, `fasrcsw-rpmbuild-Comp`, and `fasrcsw-rpmbuild-MPI`.
Putting all this together, to try building the rpm, run the following:

``` bash
fasrcsw-rpmbuild-$TYPE --define 'trial yes' -ba "$NAME-$VERSION-$RELEASE".spec
```

Eventually, after a few iterations of running the above and tweaking the spec file in order to get the software to build properly and even get to the *trial* step, the output will show something like this near the end:

```
*************** fasrcsw -- STOPPING due to %define trial yes ******************


Look at the tree output below to decide how to finish off the spec file.  (`Bad
exit status' is expected in this case, it's just a way to stop NOW.)


/home/me/rpmbuild/BUILDROOT/amhello-1.0-fasrc01.x86_64//n/sw/fasrcsw/apps/Core/amhello/1.0-fasrc01
|-- README
|-- bin
|   `-- hello
`-- share
	`-- doc
		`-- amhello
			`-- README

4 directories, 3 files


Some suggestions of what to use in the modulefile:


prepend_path("PATH",               "%{_prefix}/bin")


******************************************************************************


error: Bad exit status from /var/tmp/rpm-tmp.B5l2ZA (%install)
```

The `Bad exit status` is expected in this case.
The `README` and other docs in the root of the installation is something manually done by fasrcsw just out of personal preference.

The `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts loop over the corresponding modules to be built against.
To debug just one combination, see [this FAQ item](FAQ.md#how-do-i-build-against-just-one-compiler-or-mpi-implementation-instead-of-all).


## Finish the spec file

Re-open the spec file for editing:

``` bash
$EDITOR "$NAME-$VERSION-$RELEASE".spec
```

and, based upon the output in the previous step, write what goes in `modulefile.lua`.
Some common things are already there as comments (`--` delimits a comment in lua).


## Build the rpm(s)

Now the rpm (or set of rpms) can be fully built:

``` bash
fasrcsw-rpmbuild-$TYPE -ba "$NAME-$VERSION-$RELEASE".spec
```

Once that runs successfully, double check that all worked as expected.
For a Core app, only one rpm is built, but for Comp and MPI apps, multiple rpms are built.
There are three helpers that print the names of the rpms that should've been built -- `fasrcsw-list-Core-rpms`, `fasrcsw-list-Comp-rpms`, and `fasrcsw-list-MPI-rpms`.

``` bash
fasrcsw-rpm -qilp $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE") | less
```

(Add  --scripts to also see how the module file symlink is created in the `%postinstall`.)
For each package make sure:

* all the metadata looks good
* the `Relocations` and all files are under an app-specific prefix under `$FASRCSW_PROD`. 

Test if the rpm(s) will install okay:

``` bash
sudo -E fasrcsw-rpm -ivh --nodeps --oldpackage --test $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE")
```


## Install the rpm(s)

Finally, install the rpm(s):

``` bash
sudo -E fasrcsw-rpm -ivh --nodeps --oldpackage $(fasrcsw-list-$TYPE-rpms "$NAME-$VERSION-$RELEASE")
```

Check that the rpm(s) installed and the module(s) is/are there.
For a *Core* app:

``` bash
fasrcsw-rpm -qa | grep "$NAME-$VERSION-$RELEASE"
ls "$FASRCSW_PROD/apps/Core/$NAME/$VERSION-$RELEASE/"
module avail
module load $NAME/$VERSION-$RELEASE
#...test the app itself (for amhello, run `hello')...
module unload $NAME/$VERSION-$RELEASE
```

If you want to erase and retry the rpm(s), see [this FAQ item](FAQ.md#how-do-i-remove-apps).


## Save your work

If you're just trying things out with `amhello`, [erase the rpm(s)](FAQ.md#how-do-i-remove-apps) and remove your spec file.
Otherwise, for production apps:

Copy the rpms to the production location:

``` bash
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SOURCES/
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/RPMS/
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SRPMS/
```

Add, commit, and push all your modifications to the fasrcsw git remote with something like the following:

``` bash
cd "$FASRCSW_DEV"
git add .
git commit -v .
git pull
git push
```

And, as root, pull them to the production clone:

``` bash
cd "$FASRCSW_PROD"
sudo git pull
```
