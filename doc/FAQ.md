# Basics


### What are the naming conventions and restrictions for an app's NAME, VERSION, and RELEASE?

None of these variables may contain whitespace or shell metacharacters.
NAME and VERSION may not contain hyphens/dashes/"-".
RELEASE should be of the form `ORG##` where `ORG` is a tag identifying your organization and `##` is a two-digit number, starting from `01`.
The documentation and templates use `fasrc` for `ORG`.

It's very highly desirable that the set of NAME-VERSION-RELEASEs for an app is chronological when sorted alphanumerically.
In particular, the default module is the last version when shorted alphanumerically and should be the most recent.


### Why is a compiler a Core app and not a Comp app?  Why is an MPI implementation a Comp app and not an MPI app?

The app classifications used by fasrcsw and the module hierarchy describe the app's *dependencies*, not the app itself.
They mainly pertain to the layout in the filesystem.

An app *family* is something a bit different.
That's used by lmod to ensure only one instance of a family is loaded at a time and that proper swapping of dependencies happens when a family instance is swapped.
A compiler *is* part of the Comp *family*, and an MPI app *is* a part of the MPI *family*.



# App building


### How do I handle apps that insist on writing directly to the production location?

RPM building requires installing to a temporary location rather than the true prefix (e.g. with `make install DESTDIR=%{buildroot}`).
Some apps don't respect this or otherwise want to write directly to the production location.
In this case, when building you'll get `Permission denied` errors and see that it was attempting to write directly to `$FASRCSW_PROD/apps`.
You can hack around this in a very ugly way by replacing the template's `make install` snippet with:

``` bash
#
# This app insists on writing directly to the prefix.  Acquiesce, and hack a 
# symlink, IN THE PRODUCTION DESTINATION (yuck), back to our where we want it
# to install in our build environment, and then remove the symlink.  Note that 
# this will only work for the first build of this NAME/VERSION/RELEASE/TYPE 
# combination.
#

# Standard stuff.
umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

# Make the symlink.
sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"

make install

# Clean up the symlink.  (The parent dir may be left over, oh well.)
sudo rm "%{_prefix}"
```

Also, add this to the top of the spec file, so that you don't get any failures from /usr/lib/rpm/check-buildroot if the production location is referenced with the build outputs:

``` spec
# The spec involves the hack that allows the app to write directly to the 
# production location.  The following allows the production location path to be 
# used in files that the rpm builds.
%define __arch_install_post %{nil}
```

In the future, fasrcsw may take advantage of mock for this situation.


### How do I use one spec file to handle all compiler and MPI implementations?

The compiler modules set variables such as `CC`, `CXX`, etc., so for nicely packaged software that gets configuration information from the environment, one block of build code will often suffice.

For more complicated situations, you can use bash shell code in the rpm scriptlets and branch for each case.
If you're building a *Comp* app, i.e. using `fasrcsw-rpmbuild-Comp`, the environment variables:

* `FASRCSW_COMP_NAME`
* `FASRCSW_COMP_VERSION`
* `FASRCSW_COMP_RELEASE`

are available to use for branch tests.
If you're building an *MPI* app, these environment variables are also available:

* `FASRCSW_MPI_NAME`
* `FASRCSW_MPI_VERSION`
* `FASRCSW_MPI_RELEASE`


### How do I build against just one compiler or MPI implementation instead of all?

The `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts are just simple loops to build against all the standard compiler and MPI apps.
Sometimes only one of these is having issues building and you want to just attempt building that combination.
To do so, you can call `fasrcsw-rpmbuild-Core` directly with the appropriate compiler and, if applicable, MPI options, e.g.:

``` bash
fasrcsw-rpmbuild-Core \
  --define 'comp_name intel' --define 'comp_version 13.0.079' --define 'comp_release fasrc01' \
  --define 'mpi_name openmpi' --define 'mpi_version 1.7.3' --define 'mpi_release fasrc01' \
  -ba `$NAME-$VERSION-$RELEASE.spec`
```

Note that the `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts echo out the above such commands that they run, so use those a reference.

Since the fasrcsw system is designed to build apps against *all* relevant combinations, so be sure to run the main `fasrcsw-rpmbuild-Comp` or `fasrcsw-rpmbuild-MPI` script after you've solved the issue with the specific combination.


### How do I configure the default sets of compiler and MPI implementations used to build apps?

The arrays `FASRCSW_COMPS` and `FASRCSW_MPIS` in `setup.sh` define these.
Note that since these are arrays, a simple `echo $FASRCSW_COMPS` is misleading (it only prints the first), and, like all bash arrays, they cannot be exported to subshells.


### How do I package pre-built binaries?

See [this FAQ item](FAQ.md#how-do-i-compile-manually-instead-of-using-the-rpmbuild-macros) about building manually instead of using the macros.

* The `%prep` section should just unpack the files, same as if they were sources.  Alternatively, they can even be put in SOURCES pre-unpacked and `%prep` can do nothing; that's more efficient, but also more cumbersome for sharing).
* The `%build` section can be blank (aside from standard template code).
* The `%install` section can just copy files directly from `%{_topdir}/BUILD/%{name}-%{version}` (or `%{_topdir}/SOURCES/%{name}-%{version}` if pre-unpacked) to `%{buildroot}/%{_prefix}`.  If the app is packaged as a *sharball*, that execution can go here, too.

<!-- (this is now the default)
Note that rpmbuild does a lot of stripping and prelinking by default, and this often causes problems with pre-built binaries.
See `%define __os_install_post %{nil}` for skipping those steps.
-->


### How do I remove apps?

Define the `NAME`, `VERSION`, `RELEASE`, AND `TYPE` variables in your shell, as is done in the [HOWTO](HOWTO.md), and run:

``` bash
make uninstall
```


### How do I download amhello-1.0.tar.gz?

To download `amhello`, which is used as a demo in the [HOWTO](HOWTO.md), use the following command:

``` bash
curl http://ftp.gnu.org/gnu/automake/automake-1.14.tar.xz | tar --strip-components=2 -xvJf - automake-1.14/doc/amhello-1.0.tar.gz
```



# Dependencies


### How are simple app dependencies handled?

An app may require one or more other apps in order to function.
The other app(s) will need to be loaded during the rpmbuild, and the module file will need to make sure these other apps are loaded for users, too.
The fasrcsw system uses the following conventions when an app requires another app named `NAME`:

In the spec file's `%build` section:

``` lua
module load NAME/VERSION-RELEASE
```

In the module file:

``` lua
if mode()=="load" then
	if not isloaded("NAME") then
		load("NAME/VERSION-RELEASE")
	end
end
```

The module file logic above has the following advantages over a simple `prereq()` or `load()`:

* It will automatically pull in dependencies.
  * *a simple prereq, w/ or w/o version, would not*
* It does not change versions of modules previously loaded by the user.
  * *a simple load, w/ or w/o version, could*
* It does not unload other independently loaded modules upon unload.
  * *a simple load would*
  * downside: it does not unload modules loaded only by this module, either
* It does not totally restrict the requirement to a specific version that may get outdated.
  * *a simple prereq or load, w/ the version specified, would*
  * upside: allows the latest version to satisfy the requirement, which is hopefully compatible
  * downside: allows an older version than ideally desired to satisfy the requirement, even though it may not be compatible
  * you can always add `conflict()` or other tweaks if necessary
* The best known VERSION-RELEASE is recorded in both the spec file and the module file.
  * *a simple prereq or load, w/o version, would not have this*
  * it's fully documented, and rpm building is reproducible (i.e. it's not dependent on the external situation of what latest version is installed)
  * to rebuild the app using something newer/different, then make a new release (just like any other changes to the app build)
  * but users can still use the existing app with newer versions of the required app


### What if an app requires VERSION >= some value?

There is no standard answer for this yet.

You could have the required app set an environment variable and have the requiring app check it.
In this case it'd probably be better to have the environment variable note the presence of the specific required capability rather than just the version and having to apply string parsing and logic using that version.


### What if an app dependency can be satisfied by multiple alternatives?

If either app A or app B can satisfy a dependency, but A is the desired default, use something similar to the following:

``` lua
if mode()=="load" then
	if not (isloaded("A") or isloaded("B")) then
		load("A/VERSION-RELEASE")
	end
end
```


### How are app dependency hierarchies handled?

If app C requires apps A and B, and A also requires B, C should still explicitly require B, for clarity.
Note that, in the fasrcsw style of coding prerequisites, the order of C's requiring A and B will matter if A and C choose different versions of B to load if none other is loaded.


### How are rpm dependencies handled?

Not at all -- there is no coding of dependencies within the rpm packages.
Dependencies are only tracked at the module level.
If you find an rpm you want to install and need to know what else to install, look at what the module file (as written by the spec) says it requires.



# Miscellaneous


### How do I diff a spec file with the relevant version of the template spec file?

App spec files are initially created by copying the `template.spec` file.
However, the template is occasionally updated, and diffing any given spec file with the current template will include both the app-specific differences and the changes to the template since the app first appeared.
That can be confusing when you're just looking for the core procedure to build the app and want to use the latest template.

You can use git to diff the two different files from the two different versions:

``` bash
hash="$(git log --diff-filter=A --oneline -- rpmbuild/SPECS/$NAME-$VERSION-$RELEASE.spec | cut -d' ' -f1)"
git diff "$hash":rpmbuild/SPECS/template.spec ^HEAD:rpmbuild/SPECS/"$NAME-$VERSION-$RELEASE".spec
```

### How can I make building go faster?

Consider adding `%{?_smp_mflags}` after `make` (which usually just adds `-jN` where `N` is number of cores on the host).

Also consider binding the rpmbuild work dir (`%{_topdir}/BUILD`, the place where sources are unpacked and compiled) to faster storage, such as local scratch space.
You can do so with something like the following:

``` bash
mkdir -p /tmp/"$USER"/fasrcsw/BUILD
cp -a "$FASRCSW_DEV"/rpmbuild/BUILD/.gitignore /tmp/"$USER"/fasrcsw/BUILD
sudo mount -o bind /tmp/"$USER"/fasrcsw/BUILD "$FASRCSW_DEV"/rpmbuild/BUILD
```

### What are the values of the rpm-specific variables?

* `%{_topdir}` is `"$FASRCSW_DEV"/rpmbuild`
* `%{_prefix}` is `"$FASRCSW_PROD"/apps/{Core,Comp,MPI}/...(dependency dirs if non-Core).../%{name}/%{version}-%{release}`
* `%{buildroot}` is `$HOME/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{arch}`

See the FAQ below about why `%{buildroot}` uses your `$HOME` instead of `$FASRCSW_DEV`.


### Why is rpmbuild still writing to my home directory?

You may notice that `rpmbuild` still uses `~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}` even though everything else is self-contained within the fasrcsw clone's `%{_topdir}`.
This is part of the design of rpmbuild -- the spec file cannot override the `%{buildroot}` or `%{_buildrootdir}` variable, and by default it points to a location within your home directory.
You can provide `--buildroot` on the `rpmbuild` command line if you want, but be sure to use something app-specific as this location is `rm -fr`'ed during the build.


### Can I install the apps under a common prefix?

No.
Although all the rpms created by fasrcsw are relocatable and therefore can be installed in non-default locations by using `rpm --prefix ...`, each app owns all the files within its prefix.
Thus each app would be competing for ownership of `bin`, `lib`, etc.

However, it's not to hard to update a spec file to avoid this.
In the `%files` section, instead of using just `%{_prefix}/*`, use:

``` spec
%{_prefix}/bin/*
%{_prefix}/lib/*
...
```

And, earlier in the `%install` section, take out the for-loop that copies `COPYING`, `README`, etc. to the root of the prefix (or otherwise allow rpm to ignore these files that will not be part of the final package).


### What about easybuild?

From a cursory look, its support of lmod appears to be minimal.
In particular, it does not support module hierarchies.


### What about mock?

Good question.
The fasrcsw system does not use mock, but it's possible it could benefit from doing so.
