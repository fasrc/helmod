#------------------- package info ----------------------------------------------
#
#
# enter the simple app name, e.g. myapp
#
Name: %{getenv:NAME}

#
# enter the app version, e.g. 0.0.1
#
Version: %{getenv:VERSION}

#
# enter the release; start with fasrc01 (or some other convention for your
# organization) and increment in subsequent releases
#
# the actual "Release", %%{release_full}, is constructed dynamically; for Comp
# and MPI apps, it will include the name/version/release of the apps used to
# build it and will therefore be very long
#
%define release_short %{getenv:RELEASE}

#
# enter your FIRST LAST <EMAIL>
#
Packager: %{getenv:FASRCSW_AUTHOR}

#
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo
# rpm gets created, so this stores it separately for later re-use); do not
# surround this string with quotes
#
%define summary_static Correct, reproducible, fast builds for everyone
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if
# applicable
#
URL: http://bazel.io
Source: %{name}-%{version}.tar.gz

#
# there should be no need to change the following
#

#these fields are required by RPM
Group: fasrcsw
License: see COPYING file or upstream packaging

#this comes here since it uses Name and Version but dynamically computes Release, Prefix, etc.
%include fasrcsw_defines.rpmmacros

Release: %{release_full}
Prefix: %{_prefix}


#
# Macros for setting app data
# The first set can probably be left as is
# the nil construct should be used for empty values
#
%define modulename %{name}-%{version}-%{release_short}
%define appname %(test %{getenv:APPNAME} && echo "%{getenv:APPNAME}" || echo "%{name}")
%define appversion %(test %{getenv:APPVERSION} && echo "%{getenv:APPVERSION}" || echo "%{version}")
%define appdescription %{summary_static}
%define type %{getenv:TYPE}
%define specauthor %{getenv:FASRCSW_AUTHOR}
%define builddate %(date)
%define buildhost %(hostname)
%define buildhostversion 1
%define compiler %( if [[ %{getenv:TYPE} == "Comp" || %{getenv:TYPE} == "MPI" ]]; then if [[ -n "%{getenv:FASRCSW_COMPS}" ]]; then echo "%{getenv:FASRCSW_COMPS}"; fi; else echo "system"; fi)
%define mpi %(if [[ %{getenv:TYPE} == "MPI" ]]; then if [[ -n "%{getenv:FASRCSW_MPIS}" ]]; then echo "%{getenv:FASRCSW_MPIS}"; fi; else echo ""; fi)


%define builddependencies gcc/4.8.2-fasrc01 jdk/1.8.0_45-fasrc01
%define rundependencies %{builddependencies}
%define buildcomments %{nil}
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags %{nil}
%define apppublication %{nil}


%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.
Built on 03-30-2016 from git commit: 787abf9

%prep

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD
rm -rf %{name}-%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}.tar.*
cd %{name}-%{version}
chmod -Rf a+rX,u+w,g-w,o-w .


%build

%include fasrcsw_module_loads.rpmmacros

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}

# fix stupid environment issue
cat <<EOF | patch -p1
diff --git a/src/main/java/com/google/devtools/build/lib/shell/Command.java b/src/main/java/com/google/devtools/build/lib/shell/Command.java
index 8d9cffc..23f6377 100644
--- a/src/main/java/com/google/devtools/build/lib/shell/Command.java
+++ b/src/main/java/com/google/devtools/build/lib/shell/Command.java
@@ -200,7 +200,7 @@ public final class Command {
     if (environmentVariables != null) {
       // TODO(bazel-team) remove next line eventually; it is here to mimic old
       // Runtime.exec() behavior
-      this.processBuilder.environment().clear();
+      //this.processBuilder.environment().clear();
       this.processBuilder.environment().putAll(environmentVariables);
     }
     this.processBuilder.directory(workingDirectory);
EOF

# configure CROSSTOOL
GCC_PATH=$(which gcc)
CPP_PATH=$(which cpp)
GCC_MODULE_ROOT=$(readlink -f "$(dirname $GCC_PATH)/..")

cat <<EOF | patch -p1
diff --git a/tools/cpp/CROSSTOOL b/tools/cpp/CROSSTOOL
index 269edea..fdd22fd 100644
--- a/tools/cpp/CROSSTOOL
+++ b/tools/cpp/CROSSTOOL
@@ -86,18 +86,24 @@ toolchain {

   tool_path { name: "ar" path: "/usr/bin/ar" }
   tool_path { name: "compat-ld" path: "/usr/bin/ld" }
-  tool_path { name: "cpp" path: "/usr/bin/cpp" }
+  tool_path { name: "cpp" path: "$CPP_PATH" }
   tool_path { name: "dwp" path: "/usr/bin/dwp" }
-  tool_path { name: "gcc" path: "/usr/bin/gcc" }
+  tool_path { name: "gcc" path: "$GCC_PATH" }
   cxx_flag: "-std=c++0x"
   linker_flag: "-lstdc++"
-  linker_flag: "-B/usr/bin/"
+  linker_flag: "-B${GCC_MODULE_ROOT}/bin/"
+  linker_flag: "-Wl,-rpath,${GCC_MODULE_ROOT}/lib64"
+  linker_flag: "-Wl,-rpath,${MPC_LIB}"
+  linker_flag: "-Wl,-rpath,${MPFR_LIB}"
+  linker_flag: "-Wl,-rpath,${GMP_LIB}"

   # TODO(bazel-team): In theory, the path here ought to exactly match the path
   # used by gcc. That works because bazel currently doesn't track files at
   # absolute locations and has no remote execution, yet. However, this will need
   # to be fixed, maybe with auto-detection?
-  cxx_builtin_include_directory: "/usr/lib/gcc/"
+  cxx_builtin_include_directory: "${GCC_MODULE_ROOT}/lib64/gcc"
+  cxx_builtin_include_directory: "${GCC_MODULE_ROOT}/include"
+  cxx_builtin_include_directory: "${JAVA_HOME}/include"
   cxx_builtin_include_directory: "/usr/local/include"
   cxx_builtin_include_directory: "/usr/include"
   tool_path { name: "gcov" path: "/usr/bin/gcov" }
EOF

./compile.sh

%install

%include fasrcsw_module_loads.rpmmacros

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}/bin
cp output/bazel %{buildroot}/%{_prefix}/bin/

for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	test -e "$f" && ! test -e '%{buildroot}/%{_prefix}/'"$f" && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

%if %{defined trial}
	set +x

	echo
	echo
	echo "*************** fasrcsw -- STOPPING due to %%define trial yes ******************"
	echo
	echo "Look at the tree output below to decide how to finish off the spec file.  (\`Bad"
	echo "exit status' is expected in this case, it's just a way to stop NOW.)"
	echo
	echo

	tree '%{buildroot}/%{_prefix}'

	echo
	echo
	echo "Some suggestions of what to use in the modulefile:"
	echo
	echo

	generate_setup.sh --action echo --format lmod --prefix '%%{_prefix}'  '%{buildroot}/%{_prefix}'

	echo
	echo
	echo "******************************************************************************"
	echo
	echo

	#make the build stop
	false

	set -x
%endif

mkdir -p %{buildroot}/%{_prefix}
cat > %{buildroot}/%{_prefix}/modulefile.lua <<EOF
local helpstr = [[
%{name}-%{version}-%{release_short}
%{summary_static}
%{buildcomments}
]]
help(helpstr,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}-%{release_short}")
whatis("Description: %{summary_static}")

---- prerequisite apps (uncomment and tweak if necessary)
for i in string.gmatch("%{rundependencies}","%%S+") do
    if mode()=="load" then
        a = string.match(i,"^[^/]+")
        if not isloaded(a) then
            load(i)
        end
    end
end


---- environment changes (uncomment what is relevant)
prepend_path("PATH",                "%{_prefix}/bin")
EOF

#------------------- App data file
cat > $FASRCSW_DEV/appdata/%{modulename}.%{type}.dat <<EOF
appname             : %{appname}
appversion          : %{appversion}
description         : %{appdescription}
tags                : %{apptags}
publication         : %{apppublication}
modulename          : %{modulename}
type                : %{type}
compiler            : %{compiler}
mpi                 : %{mpi}
specauthor          : %{specauthor}
builddate           : %{builddate}
buildhost           : %{buildhost}
buildhostversion    : %{buildhostversion}
builddependencies   : %{builddependencies}
rundependencies     : %{rundependencies}
buildcomments       : %{buildcomments}
requestor           : %{requestor}
requestref          : %{requestref}
EOF


#------------------- %%files (there should be no need to change this ) --------

%files

%defattr(-,root,root,-)

%{_prefix}/*



#------------------- scripts (there should be no need to change these) --------


%pre
#
# everything in fasrcsw is installed in an app hierarchy in which some
# components may need creating, but no single rpm should own them, since parts
# are shared; only do this if it looks like an app-specific prefix is indeed
# being used (that's the fasrcsw default)
#
echo '%{_prefix}' | grep -q '%{name}.%{version}' && mkdir -p '%{_prefix}'
#

%post
#
# symlink to the modulefile installed along with the app; we want all rpms to
# be relocatable, hence why this is not a proper %%file; as with the app itself,
# modulefiles are in an app hierarchy in which some components may need
# creating
#
mkdir -p %{modulefile_dir}
ln -s %{_prefix}/modulefile.lua %{modulefile}
#


%preun
#
# undo the module file symlink done in the %%post; do not rmdir
# %%{modulefile_dir}, though, since that is shared by multiple apps (yes,
# orphans will be left over after the last package in the app family
# is removed)
#
test -L '%{modulefile}' && rm '%{modulefile}'
#

%postun
#
# undo the last component of the mkdir done in the %%pre (yes, orphans will be
# left over after the last package in the app family is removed); also put a
# little protection so this does not cause problems if a non-default prefix
# (e.g. one shared with other packages) is used
#
test -d '%{_prefix}' && echo '%{_prefix}' | grep -q '%{name}.%{version}' && rmdir '%{_prefix}'
#


%clean
#
# wipe out the buildroot, but put some protection to make sure it isn't
# accidentally / or something -- we always have "rpmbuild" in the name
#
echo '%{buildroot}' | grep -q 'rpmbuild' && rm -rf '%{buildroot}'
#
