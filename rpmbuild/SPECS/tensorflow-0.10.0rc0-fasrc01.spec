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
%define summary_static TensorFlow version 0.10.0-RC0
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if
# applicable
#
#URL: http://...FIXME...
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

%description
TensorFlow is an open source software library for numerical computation using
data flow graphs. Nodes in the graph represent mathematical operations, while
the graph edges represent the multidimensional data arrays (tensors)
communicated between them. The flexible architecture allows you to deploy
computation to one or more CPUs or GPUs in a desktop, server, or mobile device
with a single API. TensorFlow was originally developed by researchers and
engineers working on the Google Brain Team within Google's Machine Intelligence
research organization for the purposes of conducting machine learning and deep
neural networks research, but the system is general enough to be applicable in
a wide variety of other domains as well.
Built from git on 09-02-2016 using commit: 3cb3995

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


%define builddependencies bazel/20160330-fasrc01 %{rundependencies}
%define rundependencies gcc/4.8.2-fasrc01 Anaconda/2.5.0-fasrc01 cuda/7.5-fasrc01 cudnn/7.0-fasrc01
%define buildcomments %{nil}
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags %{nil}
%define apppublication %{nil}


%prep

%include fasrcsw_module_loads.rpmmacros

%define python_version $(python -c 'import sys; print "python%s.%s" % sys.version_info[0:2]')
%define site_packages %{buildroot}/%{_prefix}/lib/%{python_version}/site-packages

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

# configure CROSSTOOL

GCC_PATH=$(which gcc)
CPP_PATH=$(which cpp)
GCC_MODULE_ROOT=$(readlink -f "$(dirname $(which gcc))/..")

cat <<EOF | patch -p1
diff --git a/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc b/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc
index 04ab50c..e815d0c 100755
--- a/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc
+++ b/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc
@@ -45,12 +45,12 @@ import pipes
 
 # "configure" uses the specific format to substitute the following string.
 # If you change it, make sure you modify "configure" as well.
-CPU_COMPILER = ('/usr/bin/gcc')
-GCC_HOST_COMPILER_PATH = ('/usr/bin/gcc')
+CPU_COMPILER = ('$GCC_PATH')
+GCC_HOST_COMPILER_PATH = ('$GCC_PATH')
 
 CURRENT_DIR = os.path.dirname(sys.argv[0])
 NVCC_PATH = CURRENT_DIR + '/../../../cuda/bin/nvcc'
-LLVM_HOST_COMPILER_PATH = ('/usr/bin/gcc')
+LLVM_HOST_COMPILER_PATH = ('$GCC_PATH')
 PREFIX_DIR = os.path.dirname(GCC_HOST_COMPILER_PATH)
 
 def Log(s):
@@ -281,9 +281,6 @@ def InvokeNvcc(argv, log=False):
          ' -I .' +
          ' -x cu ' + opt + includes + ' -c ' + srcs + out)
 
-  # TODO(zhengxq): for some reason, 'gcc' needs this help to find 'as'.
-  # Need to investigate and fix.
-  cmd = 'PATH=' + PREFIX_DIR + ' ' + cmd
   if log: Log(cmd)
   return os.system(cmd)
 
EOF

cat <<EOF | patch -p1
diff --git a/third_party/gpus/crosstool/CROSSTOOL b/third_party/gpus/crosstool/CROSSTOOL
index dfde7cd..d3dfed7 100644
--- a/third_party/gpus/crosstool/CROSSTOOL
+++ b/third_party/gpus/crosstool/CROSSTOOL
@@ -36,23 +36,26 @@ toolchain {

   tool_path { name: "ar" path: "/usr/bin/ar" }
   tool_path { name: "compat-ld" path: "/usr/bin/ld" }
-  tool_path { name: "cpp" path: "/usr/bin/cpp" }
+  tool_path { name: "cpp" path: "${CPP_PATH}" }
   tool_path { name: "dwp" path: "/usr/bin/dwp" }
   # As part of the TensorFlow release, we place some cuda-related compilation
   # files in third_party/gpus/crosstool/clang/bin, and this relative
   # path, combined with the rest of our Bazel configuration causes our
   # compilation to use those files.
   tool_path { name: "gcc" path: "clang/bin/crosstool_wrapper_driver_is_not_gcc" }
   # Use "-std=c++11" for nvcc. For consistency, force both the host compiler
   # and the device compiler to use "-std=c++11".
   cxx_flag: "-std=c++11"
   linker_flag: "-lstdc++"
-  linker_flag: "-B/usr/bin/"
+  linker_flag: "-B${GCC_MODULE_ROOT}/bin/"

   # TODO(bazel-team): In theory, the path here ought to exactly match the path
   # used by gcc. That works because bazel currently doesn't track files at
   # absolute locations and has no remote execution, yet. However, this will need
   # to be fixed, maybe with auto-detection?
-  cxx_builtin_include_directory: "/usr/lib/gcc/"
+  cxx_builtin_include_directory: "${GCC_MODULE_ROOT}/lib64/gcc"
+  cxx_builtin_include_directory: "${GCC_MODULE_ROOT}/include"
+  cxx_builtin_include_directory: "${CUDA_HOME}/include"
+  cxx_builtin_include_directory: "${CUDNN_HOME}/include"
   cxx_builtin_include_directory: "/usr/local/include"
   cxx_builtin_include_directory: "/usr/include"
   tool_path { name: "gcov" path: "/usr/bin/gcov" }
EOF

cat <<EOF | ./configure
$PYTHON_HOME/bin/python
n
y
$GCC_PATH

$CUDA_HOME

$CUDNN_HOME

EOF
bazel build -c opt --config=cuda //tensorflow/tools/pip_package:build_pip_package --verbose_failures --spawn_strategy=standalone --genrule_strategy=standalone --jobs 4
bazel-bin/tensorflow/tools/pip_package/build_pip_package $PWD/wheels


%install

%include fasrcsw_module_loads.rpmmacros

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
mkdir -p %{site_packages}
export PYTHONPATH=%{site_packages}:$PYTHONPATH
pip install --target=%{site_packages} ./wheels/%{name}-%{version}-py2-none-any.whl
# not sure why this is missing but just touch for now
touch %{site_packages}/google/__init__.py

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
prepend_path("PATH",            "%{_prefix}/bin")
prepend_path("PYTHONPATH",      "%{_prefix}/lib/%{python_version}/site-packages")
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
