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
%define summary_static TensorFlow version 1.0 (GPU)
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if
# applicable
#
URL:  https://github.com/tensorflow/tensorflow/archive/v1.0.0.tar.gz
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
NOTE: This is the GPU version - use tensorflow/1.0.0-fasrc01 for CPU-only
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

%define builddependencies bazel/0.4.3-fasrc01 %{rundependencies}
%define rundependencies Anaconda/2.5.0-fasrc01 cudnn/7.0-fasrc02
%define buildcomments This build is GPU
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

GCC_MODULE_ROOT=$(readlink -f "$(dirname $(which gcc))/..")
NVCC_PATH=$(which nvcc)

sed -i -e "s?tool_path { name: \"ar\".*?tool_path { name: \"ar\" path: \"${BINUTILS_HOME}/bin/ar\" }?" \
       -e "s?tool_path { name: \"compat-ld\".*?tool_path { name: \"compat-ld\" path: \"${BINUTILS_HOME}/bin/ld\" }?" \
       -e "s?tool_path { name: \"cpp\".*?tool_path { name: \"cpp\" path: \"${GCC_MODULE_ROOT}/bin/cpp\" }?" \
       -e "/cxx_flag: \"-std=c++11\"/a linker_flag: \"-Wl,-no-as-needed\"" \
       -e "/cxx_flag: \"-std=c++11\"/a linker_flag: \"-L${GCC_MODULE_ROOT}/lib64\"" \
       -e "s?linker_flag: \"-B/usr/bin/\"?linker_flag: \"-Wl,-rpath,${GCC_MODULE_ROOT}/lib64\"?" \
       -e "s?tool_path { name: \"ld\".*?tool_path { name: \"ld\" path: \"${BINUTILS_HOME}/bin/ld\" }?" \
       -e "s?tool_path { name: \"nm\" path.*?tool_path { name: \"nm\" path: \"${BINUTILS_HOME}/bin/nm\" }?" \
       -e "s?tool_path { name: \"objcopy\".*?tool_path { name: \"objcopy\" path: \"${BINUTILS_HOME}/bin/objcopy\" }?" \
       -e "s?tool_path { name: \"objdump\".*?tool_path { name: \"objdump\" path: \"${BINUTILS_HOME}/bin/objdump\" }?" \
       -e "s?tool_path { name: \"strip\".*?tool_path { name: \"strip\" path: \"${BINUTILS_HOME}/bin/strip\" }?" \
       -e "/cxx_builtin_include_directory: \"%{cuda_include_path}\"/a  cxx_builtin_include_directory: \"${GCC_MODULE_ROOT}/include\"" \
       -e "/cxx_builtin_include_directory: \"%{cuda_include_path}\"/a  cxx_builtin_include_directory: \"${CUDA_HOME}/include\"" \
       -e "/cxx_builtin_include_directory: \"%{cuda_include_path}\"/a  cxx_builtin_include_directory: \"${CUDA_HOME}/targets/x86_64-linux/include\"" \
       -e "/cxx_builtin_include_directory: \"%{cuda_include_path}\"/a  cxx_builtin_include_directory: \"${CUDNN_HOME}/include\"" \
       -e "/cxx_builtin_include_directory: \"%{cuda_include_path}\"/a  cxx_builtin_include_directory: \"${GCC_MODULE_ROOT}/lib64/gcc\""  third_party/gpus/crosstool/CROSSTOOL.tpl


cat <<EOF | patch -p1
diff --git a/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc.tpl b/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc.tpl
index d3bb93c..237fe83 100755
--- a/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc.tpl
+++ b/third_party/gpus/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc.tpl
@@ -46,12 +46,12 @@ import sys
 import pipes
 
 # Template values set by cuda_autoconf.
-CPU_COMPILER = ('%{cpu_compiler}')
-GCC_HOST_COMPILER_PATH = ('%{gcc_host_compiler_path}')
+CPU_COMPILER = ('${GCC_MODULE_ROOT}/bin/gcc')
+GCC_HOST_COMPILER_PATH = ('${GCC_MODULE_ROOT}/bin/gcc')
 
 CURRENT_DIR = os.path.dirname(sys.argv[0])
-NVCC_PATH = CURRENT_DIR + '/../../../cuda/bin/nvcc'
-LLVM_HOST_COMPILER_PATH = ('/usr/bin/gcc')
+NVCC_PATH = '${NVCC_PATH}'
+LLVM_HOST_COMPILER_PATH = ('${GCC_MODULE_ROOT}/bin/gcc')
 PREFIX_DIR = os.path.dirname(GCC_HOST_COMPILER_PATH)
 
 def Log(s):
@@ -219,7 +219,7 @@ def InvokeNvcc(argv, log=False):
 
   # TODO(zhengxq): for some reason, 'gcc' needs this help to find 'as'.
   # Need to investigate and fix.
-  cmd = 'PATH=' + PREFIX_DIR + ' ' + cmd
+  # cmd = 'PATH=' + PREFIX_DIR + ' ' + cmd
   if log: Log(cmd)
   return os.system(cmd)
 
EOF

cat <<EOF | patch -p1
diff --git a/tensorflow/contrib/cmake/external/protobuf.cmake b/tensorflow/contrib/cmake/external/protobuf.cmake
index 5ee6987..3e3b32c 100644
--- a/tensorflow/contrib/cmake/external/protobuf.cmake
+++ b/tensorflow/contrib/cmake/external/protobuf.cmake
@@ -1,8 +1,8 @@
 include (ExternalProject)

 set(PROTOBUF_INCLUDE_DIRS \${CMAKE_CURRENT_BINARY_DIR}/protobuf/src/protobuf/src)
-set(PROTOBUF_URL https://github.com/mrry/protobuf.git)  # Includes MSVC fix.
-set(PROTOBUF_TAG 1d2c7b6c7376f396c8c7dd9b6afd2d4f83f3cb05)
+set(PROTOBUF_URL https://github.com/fasrc/protobuf.git)  # Includes MSVC fix.
+set(PROTOBUF_TAG 7e607c28815ea506b767ee8d105ffdec41ea8362)

 if(WIN32)
   set(protobuf_STATIC_LIBRARIES ${CMAKE_CURRENT_BINARY_DIR}/protobuf/src/protobuf/${CMAKE_BUILD_TYPE}/libprotobuf.lib)

EOF


cat <<EOF | patch tensorflow/workspace.bzl
203,204c203
<           "http://bazel-mirror.storage.googleapis.com/github.com/google/protobuf/archive/008b5a228b37c054f46ba478ccafa5e855cb16db.tar.gz",
<           "https://github.com/google/protobuf/archive/008b5a228b37c054f46ba478ccafa5e855cb16db.tar.gz",
---
>           "http://github.com/fasrc/protobuf/archive/b9c7df303854bbeb4eb54bc83d679fb0f8ca180c.tar.gz"
206,207c205,206
<       sha256 = "2737ad055eb8a9bc63ed068e32c4ea280b62d8236578cb4d4120eb5543f759ab",
<       strip_prefix = "protobuf-008b5a228b37c054f46ba478ccafa5e855cb16db",
---
>       sha256 = "b80bc6a4c394b14c6523169fc6f46d79cdb12ad15bc9fa234c222525b5049e42",
>       strip_prefix = "protobuf-b9c7df303854bbeb4eb54bc83d679fb0f8ca180c",

EOF

cat <<EOF | patch -p1
diff --git a/tensorflow/tensorflow.bzl b/tensorflow/tensorflow.bzl
index d78cb7b..259a6e9 100644
--- a/tensorflow/tensorflow.bzl
+++ b/tensorflow/tensorflow.bzl
@@ -792,7 +792,7 @@ def tf_custom_op_library(name, srcs=[], gpu_srcs=[], deps=[]):
   )

 def tf_extension_linkopts():
-  return []  # No extension link opts
+  return ["-lrt"]  # No extension link opts

 def tf_extension_copts():
   return []  # No extension c opts
EOF

# NOTE: 6.x only supported in cuda 8+ and tensorflow only supports 3+
NVIDIA_COMPUTE_CAPABILITIES="5.2,3.7,3.5"

# move ~/.cache/bazel - unfortunately they only have this for 'testing'
export TEST_TMPDIR="${FASRCSW_DEV}"/rpmbuild/BUILD/bazel-cache

cat <<EOF | patch configure
524a525,535
> cat <<XOF
> Python bin \$PYTHON_BIN_PATH
> Host C compiler \$GCC_HOST_COMPILER_PATH
> Host CXX compiler \$HOST_CXX_COMPILER
> os name \$OS_NAME
> Cuda capabilities \$TF_CUDA_COMPUTE_CAPABILITIES
> cudnn install path \$CUDNN_INSTALL_PATH
> cudnn lib path \$CUDA_DNN_LIB_PATH
> cuda toolkit \$CUDA_TOOLKIT_PATH
> need cuda \$TF_NEED_CUDA
> XOF
EOF

cat <<EOF | ./configure
$PYTHON_HOME/bin/python

N
N
N
N
$PYTHON_HOME/lib/python2.7/site-packages
n
y
$GCC_PATH

$CUDA_HOME

$CUDNN_HOME
$NVIDIA_COMPUTE_CAPABILITIES

EOF

bazel build -s -c opt --config=cuda  //tensorflow/tools/pip_package:build_pip_package --verbose_failures --spawn_strategy=standalone --genrule_strategy=standalone --jobs $(egrep -c 'processor\s+:' /proc/cpuinfo)
bazel-bin/tensorflow/tools/pip_package/build_pip_package $PWD/wheels


%install

%include fasrcsw_module_loads.rpmmacros

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
mkdir -p %{site_packages}
export PYTHONPATH=%{site_packages}:$PYTHONPATH
pip install --target=%{site_packages} ./wheels/%{name}-%{version}-*.whl
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
