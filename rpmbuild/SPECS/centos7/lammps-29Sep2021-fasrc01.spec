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
%define summary_static LAMMPS Molecular Dynamics Simulator 
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://download.lammps.org/tars/lammps-stable.tar.gz
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

%define builddependencies cmake/3.17.3-fasrc01 fftw/3.3.9-fasrc01 ffmpeg/4.0.2-fasrc01 netcdf/4.8.0-fasrc03 netcdf-fortran/4.5.3-fasrc03 intel/21.2.0-fasrc01 python/3.8.5-fasrc01
%define rundependencies cmake/3.17.3-fasrc01 fftw/3.3.9-fasrc01 ffmpeg/4.0.2-fasrc01 netcdf/4.8.0-fasrc03 netcdf-fortran/4.5.3-fasrc03 intel/21.2.0-fasrc01 python/3.8.5-fasrc01
%define buildcomments %{nil}
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
LAMMPS is a classical molecular dynamics code with a focus on materials modeling. It's an acronym for Large-scale Atomic/Molecular Massively Parallel Simulator.

This build includes everything but USER-QUIP and GPU.

#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep


#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things -- hopefully it'll just work as-is.
#

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD 
rm -rf %{name}-%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}.tar.*
cd %{name}-%{version}
chmod -Rf a+rX,u+w,g-w,o-w .



#------------------- %%build (~ configure && make) ----------------------------

%build

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
# FIXME
#
# configure and make the software here.  The default below is for standard 
# GNU-toolchain style things -- hopefully it'll just work as-is.
# 

##prerequisite apps (uncomment and tweak if necessary).  If you add any here, 
##make sure to add them to modulefile.lua below, too!
#module load NAME/VERSION-RELEASE

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}

# Make the symlink.
sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
sudo ln -s "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version} "%{_prefix}"

cd %{_prefix}

#cd src
#make lib-qmmm args="-m mpi"
#cd ..

rm -rf build
mkdir build
cd build

#cmake -C ../cmake/presets/all_on.cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DDOWNLOAD_LATTE=ON -DDOWNLOAD_KIM=ON -DDOWNLOAD_VORO=ON -DDOWNLOAD_EIGEN3=ON -DDOWNLOAD_MSCG=ON -DNETCDF_LIBRARY=${NETCDF_LIB} -DNETCDF_INCLUDE_DIR=${NETCDF_INCLUDE} -DQE_INCLUDE_DIR=${QE_HOME}/include -DQECOUPLE_LIBRARY=${QE_HOME}/COUPLE/include -DQEMOD_LIBRARY=${QE_HOME}/Modules -DQEFFT_LIBRARY=${QE_HOME}/FFTXlib -DQELA_LIBRARY=${QE_HOME}/LAXlib -DPW_LIBRARY=${QE_HOME}/PW -DCLIB_LIBRARY=${QE_HOME}/clib -DIOTK_LIBRARY=${QE_HOME}/iotk -DTBB_LIBRARY=${TBB_LIB} -DTBB_INCLUDE_DIR=${TBB_INCLUDE} -DTBB_MALLOC_LIBRARY=${TBB_LIB} -DKOKKOS_ENABLE_OPENMP=yes -DPKG_GPU=no -DPKG_USER-QUIP=no -DPKG_USER-ADIOS=no ../cmake 

cmake -C ../cmake/presets/basic.cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -D BUILD_SHARED_LIBS=on -D LAMMPS_EXCEPTIONS=on -D PKG_PYTHON=on -D BUILD_MPI=yes -D BUILD_OMP=yes -D LAMMPS_MACHINE=mpi -DNETCDF_LIBRARY=${NETCDF_LIB} -DNETCDF_INCLUDE_DIR=${NETCDF_INCLUDE} ../cmake
       
# -DCMAKE_INSTALL_PREFIX=%{_prefix} -DDOWNLOAD_LATTE=ON -DDOWNLOAD_KIM=ON -DDOWNLOAD_VORO=ON -DDOWNLOAD_EIGEN3=ON -DDOWNLOAD_MSCG=ON -DNETCDF_LIBRARY=${NETCDF_LIB} -DNETCDF_INCLUDE_DIR=${NETCDF_INCLUDE} -DQE_INCLUDE_DIR=${QE_HOME}/include -DQECOUPLE_LIBRARY=${QE_HOME}/COUPLE/include -DQEMOD_LIBRARY=${QE_HOME}/Modules -DQEFFT_LIBRARY=${QE_HOME}/FFTXlib -DQELA_LIBRARY=${QE_HOME}/LAXlib -DPW_LIBRARY=${QE_HOME}/PW -DCLIB_LIBRARY=${QE_HOME}/clib -DIOTK_LIBRARY=${QE_HOME}/iotk -DTBB_LIBRARY=${TBB_LIB} -DTBB_INCLUDE_DIR=${TBB_INCLUDE} -DTBB_MALLOC_LIBRARY=${TBB_LIB} -DKOKKOS_ENABLE_OPENMP=yes -DPKG_GPU=no -DPKG_USER-QUIP=no -DPKG_USER-ADIOS=no ../cmake

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel
make %{?_smp_mflags}



#------------------- %%install (~ make install + create modulefile) -----------

%install

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
# FIXME
#
# make install here.  The default below is for standard GNU-toolchain style 
# things -- hopefully it'll just work as-is.
#
# Note that DESTDIR != %{prefix} -- this is not the final installation.  
# Rpmbuild does a temporary installation in the %{buildroot} and then 
# constructs an rpm out of those files.  See the following hack if your app 
# does not support this:
#
# https://github.com/fasrc/fasrcsw/blob/master/doc/FAQ.md#how-do-i-handle-apps-that-insist-on-writing-directly-to-the-production-location
#
# %%{buildroot} is usually ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{arch}.
# (A spec file cannot change it, thus it is not inside $FASRCSW_DEV.)
#

umask 022
#cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/build
cd %{_prefix}/build
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
make install DESTDIR=%{buildroot}
rsync -av --progress %{_prefix}/build/ %{buildroot}/%{_prefix}/build/

# Clean up the symlink.  (The parent dir may be left over, oh well.)
sudo rm "%{_prefix}"

#(this should not need to be changed)
#these files are nice to have; %%doc is not as prefix-friendly as I would like
#if there are other files not installed by make install, add them here
for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	test -e "$f" && ! test -e '%{buildroot}/%{_prefix}/'"$f" && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

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
setenv("LAMMPS_HOME",       "%{_prefix}")
setenv("LAMMPS_PATH",       "%{_prefix}/bin")
setenv("LAMMPS_INCLUDE",    "%{_prefix}/include")
setenv("LAMMPS_LIB",        "%{_prefix}/lib")

prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/include")
prepend_path("FPATH",              "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/build/python/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/build/python/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib64")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/build/CMakeFiles/Export/lib64")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib64")
prepend_path("LIBRARY_PATH",       "%{_prefix}/build/CMakeFiles/Export/lib64")
prepend_path("MANPATH",            "%{_prefix}/share/man")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/lib64/pkgconfig")
prepend_path("PYTHONPATH",         "%{_prefix}/lib/python3.8/site-packages")
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
