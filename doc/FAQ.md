# Basics

### What are the naming conventions and restrictions for an app's NAME, VERSION, and RELEASE?

None of the variables may contain whitespace or shell metacharacters.
NAME and VERSION may not contain hyphens/dashes (the "-" character).
RELEASE should be of the form `fasrc##` where `##` is a two-digit number, the first one being `fasrc01`.

It's very highly desirable that the set of NAME-VERSION-RELEASEs for an app, when sorted alphanumerically, is chronological.
In particular, the default module is the last version when shorted alphanumerically and should be the most recent.



### Why is a compiler a Core app and not a Comp app?  Why is an MPI implementation a Comp app and not an MPI app?

The app families used by fasrcsw and the module hierarchy describe the app's *dependencies*, not the app itself.
An app in a certain family will get reloaded if the module representing that family is swapped.



# App building


### How do I compile manually instead of using the rpmbuild macros?

The rpmbuild macros employed in the template spec file are for software packaged in the GNU-toolchain-style -- a source archive that unpacks to a directory named NAMED-VERSION and is built with `configure`/`make`/`make install` with appropriate `prefix` options.
The macros also do a lot of extra stuff like setting default `CFLAGS`, `CXXFLAGS`, etc. too.
The macros have their own options and can often be tweaked to work.
E.g., to add an argument to the `./configure` command, you can just add it to the `%configure` macro.

However, if you need to do things manually, you can replace the macros with the following as a starting point.
Note that these are *very* stripped down versions of what the full macros actually do.

In the `%prep` section, replace:

```
%setup
```

with:

``` spec
cd %{_topdir}/BUILD
tar xvf %{_topdir}/SOURCES/%{name}-%{version}.tar.*
stat %{name}-%{version}
```

In the `%build` section, replace:

``` spec
%configure
make
```

with:

``` spec
cd %{_topdir}/BUILD/%{name}-%{version}
./configure --prefix=%{_prefix}
make
```

In the `%install` section, replace:

``` spec
%makeinstall
```

with:

``` spec
cd %{_topdir}/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
make prefix=%{buildroot}/%{_prefix} install
```

Note that `./configure` and `make install` use two different prefixes.
If `make` is still trying to install stuff directly in `%{_prefix}`, you may have to instead directly provide `%{buildroot}/%{_prefix}` to `./configure` (but that could cause trouble if any apps use rpaths).
Note also that `prefix` alone often does not cover `sysconfdir`, `sharedstatedir`, etc.; if the app uses these you'll have to add the corresponding arguments to `./configure` and `make install` (as the macros do).



### How do I use one spec file to handle all compiler and MPI implementations?

You can use bash shell code in the rpm scriptlets and branch for each case.
If you're building a *Comp* app, i.e. using `fasrcsw-rpmbuild-Comp`, the environment variables:

* `FASRCSW_COMP_NAME`
* `FASRCSW_COMP_VERSION`
* `FASRCSW_COMP_RELEASE`

are available to use for branch tests.
If you're building an *MPI* app, these environment variables are also available:

* `FASRCSW_MPI_NAME`
* `FASRCSW_MPI_VERSION`
* `FASRCSW_MPI_RELEASE`

Note that compiler modules also set variables such as `CC`, `CXX`, etc., so for nicely packaged software that gets configuration information from the environment, one block of build code will suffice, no branching necessary.


### How do I build against just one compiler or MPI implementation instead of all?

The `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts are just simple loops over the corresponding compiler and MPI modules to build against (defined in the `FASRCSW_COMPS` and `FASRCSW_MPIS` environment variables).
Sometimes only one of these is having issues building and you want to just attempt building that combination.
To do so, you can call `fasrcsw-rpmbuild-Core` directly with the appropriate compiler and, if applicable, MPI options, e.g.:

``` bash
fasrcsw-rpmbuild-Core \
  --define 'comp_name intel' --define 'comp_version 13.0.079' --define 'comp_release fasrc01' \
  --define 'mpi_name openmpi' --define 'mpi_version 1.7.3' --define 'mpi_release fasrc01' \
  -ba `$NAME-$VERSION-$RELEASE.spec`
```

Note that the `fasrcsw-rpmbuild-Comp` and `fasrcsw-rpmbuild-MPI` scripts echo out the above such commands that they run, so use those a reference.

The fasrcsw system is designed to build apps against *all* relevant combinations, so be sure to run the main `fasrcsw-rpmbuild-Comp` or `fasrcsw-rpmbuild-MPI` script after you've solved the issue with the specific dependency.


### How do I the default sets of compiler and MPI implementations used to build apps?

The bash arrays `FASRCSW_COMPS` and `FASRCSW_MPIS` in `setup.sh` define these.


### How do I deal with pre-built binaries?

See [this FAQ item](how-do-i-compile-manually-instead-of-using-the-rpmbuild-macros) about building manually instead of using the macros.

* The `%setup` section should just unpack the files, same as if they were sources.  Alternatively, they can even be put in SOURCES pre-unpacked and `%prep` can do nothing; that's is more efficient, but more cumbersome for sharing).
* The `%build` section can be blank (aside from standard template code).
* The `%install` section can just copy files directly from `%{_topdir}/BUILD/%{name}-%{version}` (or `%{_topdir}/SOURCES/%{name}-%{version}` if pre-unpacked) to `%{buildroot}/%{_prefix}`.

Note that rpmbuild does a lot of stripping and prelinking by default, and this often causes problems with pre-built binaries.



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
In this case it'd probably be better to have the environment variable note the presence of the specific required capability rather than just the version and having to apply string parsing and logic using the version.


### What if an app dependency can be satisfied by multiple alternatives?

If either app A or app B can satisfy a dependency, but A is the desired default, use something similar to the following:

``` lua
if mode()=="load" then
	if not (isloaded("appA") or isloaded("appB")) then
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



# Misc


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
