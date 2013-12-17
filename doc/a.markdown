# Overview

...TODO...

NAME, VERSION, RELEASE -- here RELEASE is fasrc## starting at fasrc01


# One-time setup

Clone the repo in some personal location, preferably on network storage, e.g. somewhere in your home directory:

	git clone git@github.com:/fasrc/fasrcsw.git ~/fasrcsw

Customize `setup.sh`, particularly `$FASRCSW_PROD`, for your environment.


# Workflow

## Intro

The following is an example of building a simple GNU autotools style software package, i.e. something that uses `configure`/`make`/`make install` with standard options.
This specifically uses the automake hello-world example, `amhello-1.0.tar.gz`, distributed with automake.

This starts by building it as a *Core* app -- one that does not depend upon compiler or MPI implementation.

## Prep

* make sure you're logged into the build host
* make sure you're logged into your normal user account, *not* root
* `cd` to your personal fasrcsw clone and setup the environment:

	source ./setup.sh

There will now be two environment variables defined that are used in the instructions below --
`$FASRCSW_DEV` is the location of your personal clone, and
`$FASRCSW_PROD` is the one, central location for your organizations's software.

## Get the source code

By whatever means necessary, get a copy of the package source archive into the location for the sources:

	cd "$FASRCSW_DEV"/rpmbuild/SOURCES
	wget --no-clobber http://...

E.g. for `amhello`, which is a bit complicated because it's a tarball within another tarball:
	
	#amhello example ONLY
	curl http://ftp.gnu.org/gnu/automake/automake-1.14.tar.xz \
	  | tar --strip-components=2 -xvJf - automake-1.14/doc/amhello-1.0.tar.gz

## Create a preliminary spec file

Change to the directory of spec files:

	cd "$FASRCSW_DEV"/rpmbuild/SPECS

Create a spec file for the app based upon the template:

	cp -ai template.spec NAME-VERSION-RELEASE.spec

Substitute `NAME-VERSION-RELEASE` with appropriate values.
If this is the first fasrcsw-style build, use `fasrc01` for the `RELEASE`; otherwise increment what already exists.
E.g. for the first `amhello` build:
	
	#amhello example ONLY
	cp -ai template.spec amhello-1.0-fasrc01.spec

Now edit the spec file and address things with the word **`FIXME`** in them.
(For some things, the default will be fine.)
Eventually all need to be addressed, but for now, you can stop at the **`%makeinstall`** line (or whatever you replace it with, if the build is not standard GNU autotools style).

## Build the software and examine its output

This above creates enough of a spec file to build the sofware, but leaves the installation configuration for later.
This is because before you can provide the installation details you almost always have to do a trial build of the app to see what it actually creates.
The template spec has a section that, if the macro `inspect` is defined, will quit the rpmbuild after the basic `make install` step and use the `tree` command to dump out what was build.
Do so:

	rpmbuild --eval '%define inspect yes' -ba NAME-VERSION-RELEASE.spec

E.g. for `amhello`:

	#amhello example ONLY
	rpmbuild --eval '%define inspect yes' -ba amhello-1.0-fasrc01.spec

and the output will show something like this near the end:



## Finish the spec file
