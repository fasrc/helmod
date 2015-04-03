# How to build and install an app


## Overview

The basic workflow to build an app using HeLmod is:

* get the source
* create and partially complete a spec file, using the template as a starting point
* do a preliminary build of the software to see what it creates, in order to know what to put in the module file
* complete the spec file and build the final rpm(s)
* install the rpm(s)
* commit changes and move the build outputs to production repos and archives

Once you're comfortable with the workflow, you can probably just use [HOWTO-short](HOWTO-short.md) instead of this doc.

The default behavior and templates are designed to work with GNU-toolchain-style software packages, i.e. things that use `configure`/`make`/`make install` with standard options, with as little modification as possible.
As an example, this document uses the automake hello-world example, `amhello-1.0.tar.gz`, distributed with automake.
If you're new to HeLmod, *try building and installing amhello first*, to get the hang of things.


## Prepare

Get ready to build software:

* make sure you've cloned and configured HeLmod according to [this](INSTALL.md#have-each-contributor-setup-a-development-repo-clone)
* make sure you're logged into the build host
* make sure you're logged into your normal user account (with sudo privilege), *not* root

`cd` to your personal HeLmod clone.
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
`RELEASE` is used to track the build under the HeLmod system and should be of the form `fasrc##` where `##` is a two-digit number.
If this is the first HeLmod-style build, use `fasrc01`; otherwise increment the fasrc number used in the previous spec file for the app.

Regarding `TYPE`, a major purpose of HeLmod is to manage entire software environments for multiple compiler and MPI implementations.
Apps are therefore categorized by their *dependencies* (see [this FAQ item](FAQ.md#why-is-a-compiler-a-core-app-and-not-a-comp-app--why-is-an-mpi-implementation-a-comp-app-and-not-an-mpi-app) more about this initially non-intuitive convention, adopted from TACC):

* A *Core* app is one that does not depend on a compiler or MPI implementation.
* A *Comp* app is one that depends upon compiler but not MPI implementation.  It's conventional to build MPI implementation apps against multiple compilers, so The MPI apps themselves are *Comp* apps.
* A *MPI* app is one that depends upon MPI implementation, and therefore upon compiler, too.

Set `TYPE` to the string `Core`, `Comp`, or `MPI`.
Unless you have a reason to build with the newer compilers or you need to build against MPI, just set `TYPE=Core` (see [this FAQ item](FAQ.md#should-an-average-app-be-a-core-app-or-a-comp-app) for more info).

For example, to test the simple *Core* case with `amhello`: `export NAME=amhello ; export VERSION=1.0 ; export RELEASE=$USER ; export TYPE=Core`.
Note that this breaks convention and uses `$USER` for the `RELEASE` instead of `fasrc01` -- this is to avoid people clobbering each other during a demo.
The `amhello` example can be used to test all app types, even though the dependencies are not real.


## Get the source code

Put a copy of the app source archive in the location for the sources.
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

and find and address all the appearances of `FIXME`.
For example, there are sections where `./configure`, `make`, and `make install` called; adjust them if necessary.
For GNU-toolchain-style software, including amhello, the template code works as-is.
Just complete everything up to where `modulefile.lua` is created (the part where you need to know what environment variables to change).
The next step will provide the necessary guidance on what to put in the module file.

If the app you're building requires other apps, follow the templates for loading the appropriate modules during the `%build` step and having the module file require them, too.
See [this FAQ item](FAQ.md#how-are-simple-app-dependencies-handled) for more details.

If the build process is different for different compilers and/or MPI implementations, see [this FAQ item](FAQ.md#how-do-i-use-one-spec-file-to-handle-all-compiler-and-mpi-implementations).



## Do a trial build and inspect its output

The result of the above will be enough of a spec file to basically build the software.
However, you have to build it and examine its output in order to know what to put in the module file that the rpm is also responsible for constructing.
Run the following to do a partial build, up to where that module file is built.
This will print suggestions for what to put there:

``` bash
make trial
```

Eventually, after a few iterations of running the above and tweaking the spec file in order to get the software to build properly and even get to the *trial* step, the output will show something like this near the end:

```
*************** helmod -- STOPPING due to %define trial yes ******************


Look at the tree output below to decide how to finish off the spec file.  (`Bad
exit status' is expected in this case, it's just a way to stop NOW.)


/home/me/helmod/rpmbuild/BUILDROOT/amhello-1.0-fasrc01.x86_64//n/sw/helmod/apps/Core/amhello/1.0-fasrc01
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
The `README` and other docs in the root of the installation is something manually done by HeLmod just out of personal preference.


## Finish the spec file

Based upon the output in the previous step, finish the spec file by writing what goes in `modulefile.lua`.
Usually this is as simple as copy-n-pasting the suggested block of text at the end of the `make trial` output.


## Build the rpm(s)

Now the rpm (or set of rpms) can be fully built:

``` bash
make
```

For a Core app, only one rpm is built, but for Comp and MPI apps, multiple rpms are built.
In the latter case, possibly only one combination is failing to build; see [this FAQ item](FAQ.md#how-do-i-build-against-just-one-compiler-or-mpi-implementation-instead-of-all) to debug just that without rebuilding the working ones each time.

Once that runs successfully, double check that all worked as expected.
You can list and inspect the rpms that were built with the following:

``` bash
make filelist
make filequery | less
```

(Add `--scripts` to the latter to see how the module file symlink is created in the `%postinstall`.)
For each package you should see that:

* all the metadata looks good
* the `Relocations` and all files are under an app-specific prefix under `$FASRCSW_PROD`. 

Test if the rpm(s) will install okay:

``` bash
make test
```

This currently only tests that the rpm is installable, and that almost never fails.
Note that it does *not* test if the loading the module or running the software actually works.


## Install the rpm(s)

Finally, install the rpm(s):

``` bash
make install
```

Check that the rpm(s) installed:

``` bash
make query
```

and the module(s) is/are there.
For a *Core* app:

``` bash
ls "$FASRCSW_PROD/apps/Core/$NAME/$VERSION-$RELEASE/"
module avail
module load $NAME/$VERSION-$RELEASE
#...test the app itself (for amhello, run `hello')...
module unload $NAME/$VERSION-$RELEASE
```

If you want to erase and retry the process, `make uninstall`.


## Save your work

If you're just trying things out with `amhello`, `make uninstall` and remove your spec file (`amhello*` is `.gitignore`d anyways).
Otherwise, for production apps, copy the rpms to the production location and commit/push all your modifications to the HeLmod git remote.
The following will do all of this:

``` bash
make post
```

For completeness, as root, pull them to the production clone:

``` bash
cd "$FASRCSW_PROD"
sudo git pull
```
