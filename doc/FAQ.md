## What are the naming conventions and restrictions for an app's NAME, VERSION, and RELEASE?

NAME and VERSION may not contain hyphens/dashes (the "-" character).
`RELEASE` should be of the form `fasrc##` where `##` is a two-digit number, the first one being `fasrc01`.

It's very highly desirable that the set of `NAME-VERSION-RELEASE`s for an app, when sorted alphanumerically, is chronological.
In particular, the default module is the last version when shorted alphanumerically and should be the most recent.


## How are app dependencies handled?

An app may require one or more other apps in order to function.
The other app(s) will need to be loaded during the rpmbuild, and the module file will need to make sure these other apps are loaded, also.
The fasrcsw system uses the following conventions when an app that requires another app named `NAME`:

In the spec `%build` section:

	module load NAME/VERSION-RELEASE

In the module file:

	if mode()=="load" then
		if not isloaded("NAME") then
			load("NAME/VERSION-RELEASE")
		end
	end

The module file logic above has the following advantages over a simple `prereq()` or `load()`:

* it will automatically pull in dependencies
  * *a simple prereq, w/ or w/o version, would not*
* it does not change versions of modules previously loaded by the user
  * *a simple load, w/ or w/o version, could*
* does not unload independently loaded modules upon unload
  * *a simple load would*
  * downside: it does not unload modules loaded only by this one, either
* it does not totally restrict the requirement to a specific version that may get outdated
  * *a simple prereq or load, w/ the version specified, specified would*
  * upside: allows the latest version to satisfy the requirement, which is hopefully compatible
  * downside: allows an older version than ideally desired to satisfy the requirement, even though it may not be compatible
  * you can always add conflict() or other tweaks if necessary
* the best known `VERSION-RELEASE` is recorded in both the spec file and the module file
  * *a simple prereq or load, w/o version, would not have this*
  * i.e. it's fully documented, and rpm building is reproducible (it's not dependent on the external situation of what the latest version is that's installed)
  * to rebuild the rpm using something newer/different, then make a new release (just like any other changes to the app build)
  * but users can still use the existing app with newer versions of the required app


## How are rpm dependencies handled?

Not at all -- there is no coding of dependencies within the rpm packages.
Dependecies are only tracked at the module level.
If you find an rpm you want to install and need to know what else to install, look at what the module file (as written by the spec) says it requires.


## Why is rpmbuild still using my home directory?

You may notice that `rpmbuild` still uses `~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}` even though everything else is self-contained within the fasrcsw clone `%{_topdir}`.
This is part of the design of rpmbuild -- the spec file cannot override the `%{buildroot}` or `%{_buildrootdir}` variable, and by default it points to a location within your home directory.
You can provide `--buildroot` on the `rpmbuild` command line if you want, but be sure to use something app-specific as this location is `rm -fr`'ed during the build.
