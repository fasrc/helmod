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
%define summary_static A high-level, high-performance dynamic programming language for technical computing.
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://github.com/JuliaLang/julia
# Source: %{name}-%{version}-full.tar.gz

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

%define builddependencies cmake/3.5.2-fasrc01 git/2.1.0-fasrc02 python/2.7.13-fasrc01 OpenBLAS/0.2.18-fasrc01 
%define rundependencies python/2.7.13-fasrc01 OpenBLAS/0.2.18-fasrc01 
%define buildcomments This Julia was built against the general compute processor architecture (JULIA_CPU_TARGET=core2) for Odyssey (i.e. general and interact partitions).  It will not work for login nodes and may not work on many nodes in serial_requeue.  Using the git release-0.5 branch due to bugs in the tarball release
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags %{nil} 
%define apppublication %{nil}



#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
Julia is a high-level, high-performance dynamic programming language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library. The library, largely written in Julia itself, also integrates mature, best-of-breed C and Fortran libraries for linear algebra, random number generation, signal processing, and string processing. In addition, the Julia developer community is contributing a number of external packages through Julia¿s built-in package manager at a rapid pace. IJulia, a collaboration between the IPython and Julia communities, provides a powerful browser-based graphical notebook interface to Julia.

%prep

%build

%include fasrcsw_module_loads.rpmmacros

%install

%include fasrcsw_module_loads.rpmmacros

echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
## Symlink the final prefix (which the build insists on using), to the 
# buildroot (the temporary place where we want to install it now).  
# Note that this will fail if this is not the first build of this 
# NAME/VERSION/RELEASE/TYPE.
sudo mkdir -p "$(dirname %{_prefix})"
sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"
%{_topdir}/SOURCES/%{name}_%{version}_387.26_linux.run -toolkit -toolkitpath="%{_prefix}" -silent
%{_topdir}/SOURCES/%{name}_%{version}.1_linux.run --installdir="%{_prefix}" --silent --accept-eula 

# Clean up that symlink.  The parent dir may be left over, oh well.
sudo rm "%{_prefix}"

## this is just because the nvidia uninstaller will keep track of the reference to the link we created in the uninstall manifest
## and this would upset /usr/lib/rpm/check-buildroot  
echo -e "g/BUILDROOT/d\nw\nq"   | ed %{buildroot}/%{_prefix}/bin/.uninstall_manifest_do_not_delete.txt 

#(this should not need to be changed)
#this is the part that allows for inspecting the build output without fully creating the rpm
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

# 
# FIXME (but the above is enough for a "trial" build)
#
# This is the part that builds the modulefile.  However, stop now and run 
# `make trial'.  The output from that will suggest what to add below.
#
# - uncomment any applicable prepend_path things (`--' is a comment in lua)
#
# - do any other customizing of the module, e.g. load dependencies -- make sure 
#   any dependency loading is in sync with the %%build section above!
#
# - in the help message, link to website docs rather than write anything 
#   lengthy here
#
# references on writing modules:
#   http://www.tacc.utexas.edu/tacc-projects/lmod/advanced-user-guide/writing-module-files
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/initial-setup-of-modules
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/module-commands-tutorial
#

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

---- environment changes (uncomment what is relevant)
setenv("CUDA_HOME",                 "%{_prefix}")
setenv("CUDA_LIB",                  "%{_prefix}/lib64")
setenv("CUDA_INCLUDE",              "%{_prefix}/include")
prepend_path("PATH",                "%{_prefix}/bin")
prepend_path("CPATH",               "%{_prefix}/include")
prepend_path("FPATH",               "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",        "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib64")
prepend_path("LIBRARY_PATH",        "%{_prefix}/lib64")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/extras/CUPTI/lib64")
prepend_path("LIBRARY_PATH",        "%{_prefix}/extras/CUPTI/lib64")

local mroot = os.getenv("MODULEPATH_ROOT")
local cudadir = pathJoin(mroot, "CUDA")
local cudapath = pathJoin("%{name}","%{version}-%{release_short}")
local mdir = pathJoin(cudadir,cudapath)
local comppath = ''
prepend_path("MODULEPATH",mdir)
if os.getenv("FASRCSW_COMP_NAME") ~= nil then
    comppath = pathJoin(os.getenv("FASRCSW_COMP_NAME"),os.getenv("FASRCSW_COMP_VERSION") .. '-' .. os.getenv("FASRCSW_COMP_RELEASE"))
    mdir = pathJoin(cudadir, comppath, cudapath)
    prepend_path("MODULEPATH",mdir)
end
if os.getenv("FASRCSW_MPI_NAME") ~= nil then
    mpipath = pathJoin(os.getenv("FASRCSW_MPI_NAME"),os.getenv("FASRCSW_MPI_VERSION") .. '-' .. os.getenv("FASRCSW_MPI_RELEASE"))
    mdir = pathJoin(cudadir, comppath, mpipath, cudapath)
    prepend_path("MODULEPATH",mdir)
end
setenv("FASRCSW_CUDA_NAME"   , "%{name}")
setenv("FASRCSW_CUDA_VERSION", "%{version}")
setenv("FASRCSW_CUDA_RELEASE", "%{release_short}")
family("CUDA")

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
