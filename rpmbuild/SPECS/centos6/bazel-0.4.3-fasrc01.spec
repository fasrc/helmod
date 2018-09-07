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
Source: %{name}-%{version}-dist.zip

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


%define builddependencies gcc/4.9.3-fasrc01 binutils/2.25.1-fasrc01 mpc/1.0.3-fasrc04 jdk/1.8.0_45-fasrc01
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
mkdir %{name}-%{version}
unzip -d %{name}-%{version} "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}-dist.zip
cd %{name}-%{version}
chmod -Rf a+rX,u+w,g-w,o-w .


%build

%include fasrcsw_module_loads.rpmmacros

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}

# configure CROSSTOOL
GCC_MODULE_ROOT=$(readlink -f "$(dirname $GCC_PATH)/..")

cat <<EOF | patch -p1
diff --git a/tools/cpp/CROSSTOOL b/tools/cpp/CROSSTOOL
index dd63b3e..bc55f03 100755
--- a/tools/cpp/CROSSTOOL
+++ b/tools/cpp/CROSSTOOL
@@ -90,34 +90,41 @@ toolchain {
   target_system_name: "local"
   toolchain_identifier: "local_linux"
 
-  tool_path { name: "ar" path: "/usr/bin/ar" }
-  tool_path { name: "compat-ld" path: "/usr/bin/ld" }
-  tool_path { name: "cpp" path: "/usr/bin/cpp" }
+  tool_path { name: "ar" path: "${BINUTILS_HOME}/bin/ar" }
+  tool_path { name: "as" path: "${BINUTILS_HOME}/bin/as" }
+  tool_path { name: "compat-ld" path: "${BINUTILS_HOME}/bin/ld" }
+  tool_path { name: "cpp" path: "${GCC_MODULE_ROOT}/bin/cpp" }
   tool_path { name: "dwp" path: "/usr/bin/dwp" }
-  tool_path { name: "gcc" path: "/usr/bin/gcc" }
+  tool_path { name: "gcc" path: "${GCC_MODULE_ROOT}/bin/gcc" }
   cxx_flag: "-std=c++0x"
   linker_flag: "-lstdc++"
-  linker_flag: "-B/usr/bin/"
+  linker_flag: "-B${GCC_MODULE_ROOT}/bin/"
+  linker_flag: "-Wl,-rpath,${GCC_MODULE_ROOT}/lib64"
+  linker_flag: "-Wl,-rpath,${MPC_HOME}/lib"
+  linker_flag: "-Wl,-rpath,${MPFR_HOME}/lib64"
+  linker_flag: "-Wl,-rpath,${GMP_HOME}/lib64"
 
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
-  tool_path { name: "gcov" path: "/usr/bin/gcov" }
+  tool_path { name: "gcov" path: "${BINUTILS_HOME}/bin/gcov" }
 
   # C(++) compiles invoke the compiler (as that is the one knowing where
   # to find libraries), but we provide LD so other rules can invoke the linker.
-  tool_path { name: "ld" path: "/usr/bin/ld" }
+  tool_path { name: "ld" path: "${BINUTILS_HOME/bin/ld" }
 
-  tool_path { name: "nm" path: "/usr/bin/nm" }
-  tool_path { name: "objcopy" path: "/usr/bin/objcopy" }
+  tool_path { name: "nm" path: "${BINUTILS_HOME}/bin/nm" }
+  tool_path { name: "objcopy" path: "${BINUTILS_HOME}/bin/objcopy" }
   objcopy_embed_flag: "-I"
   objcopy_embed_flag: "binary"
-  tool_path { name: "objdump" path: "/usr/bin/objdump" }
-  tool_path { name: "strip" path: "/usr/bin/strip" }
+  tool_path { name: "objdump" path: "${BINUTILS_HOME}/bin/objdump" }
+  tool_path { name: "strip" path: "${BINUTILS_HOME}/bin/strip" }
 
   # Anticipated future default.
   unfiltered_cxx_flag: "-no-canonical-prefixes"
EOF

cat <<EOF | patch -p1
diff --git a/tools/cpp/cc_configure.bzl b/tools/cpp/cc_configure.bzl
index 330a068..67cda8e 100755
--- a/tools/cpp/cc_configure.bzl
+++ b/tools/cpp/cc_configure.bzl
@@ -100,7 +100,7 @@ def _execute(repository_ctx, command, environment = None):
 
 def _get_tool_paths(repository_ctx, darwin, cc):
   """Compute the path to the various tools."""
-  return {k: _which(repository_ctx, k, "/usr/bin/" + k)
+  return {k: _which(repository_ctx, k, "${BINUTILS_HOME}/" + k)
           for k in [
               "ld",
               "cpp",
@@ -112,8 +112,8 @@ def _get_tool_paths(repository_ctx, darwin, cc):
               "strip",
           ]} + {
               "gcc": cc,
-              "ar": "/usr/bin/libtool"
-                    if darwin else _which(repository_ctx, "ar", "/usr/bin/ar")
+              "ar": "${BINUTILS_HOME}/libtool"
+                    if darwin else _which(repository_ctx, "ar", "${BINUTILS_HOME}/ar")
           }
 
 
@@ -221,8 +221,8 @@ def _crosstool_content(repository_ctx, cc, cpu_value, darwin):
               "-headerpad_max_install_names",
           ] if darwin else [
               "-B" + str(repository_ctx.path(cc).dirname),
-              # Always have -B/usr/bin, see https://github.com/bazelbuild/bazel/issues/760.
-              "-B/usr/bin",
+              # Always have -B${BINUTILS_HOME}, see https://github.com/bazelbuild/bazel/issues/760.
+              "-B${BINUTILS_HOME}",
               # Have gcc return the exit code from ld.
               "-pass-exit-codes",
               # Stamp the binary with a unique identifier.
@@ -259,8 +259,8 @@ def _crosstool_content(repository_ctx, cc, cpu_value, darwin):
           # Disable some that are problematic.
           "-Wl,-z,-relro,-z,now",
           "-B" + str(repository_ctx.path(cc).dirname),
-          # Always have -B/usr/bin, see https://github.com/bazelbuild/bazel/issues/760.
-          "-B/usr/bin",
+          # Always have -B${BINUTILS_HOME}, see https://github.com/bazelbuild/bazel/issues/760.
+          "-B${BINUTILS_HOME}",
       ]) + (
           _add_option_if_supported(repository_ctx, cc, "-Wunused-but-set-parameter") +
           # has false positives
EOF

cat <<EOF | patch -p1
diff --git a/third_party/protobuf/3.0.0/protobuf.bzl b/third_party/protobuf/3.0.0/protobuf.bzl
index 0e8c2e2..0d8a835 100755
--- a/third_party/protobuf/3.0.0/protobuf.bzl
+++ b/third_party/protobuf/3.0.0/protobuf.bzl
@@ -72,6 +72,7 @@ def _proto_gen_impl(ctx):
         outputs=ctx.outputs.outs,
         arguments=args + import_flags + [s.path for s in srcs],
         executable=ctx.executable.protoc,
+        use_default_shell_env=True,
     )

   return struct(
EOF

# have to bump user process limit otherwise you run into this:
# https://github.com/bazelbuild/bazel/issues/2177
ulimit -u 100000

export EXTRA_BAZEL_ARGS="-s --verbose_failures --ignore_unsupported_sandboxing --genrule_strategy=standalone --spawn_strategy=standalone --jobs $(egrep -c 'processor\s+:' /proc/cpuinfo)"

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
