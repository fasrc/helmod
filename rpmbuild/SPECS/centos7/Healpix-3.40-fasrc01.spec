#------------------- package info ----------------------------------------------

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
%define summary_static Data Analysis, Simulations and Visualization on the Sphere
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL:  http://downloads.sourceforge.net/project/healpix/Healpix_3.40/Healpix_3.40_2018Jun22.tar.gz 
Source: %{name}_%{version}_2018Jun22.tar.gz 

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
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
Software for pixelization, hierarchical indexation, synthesis, analysis, and visualization of data on the sphere.

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



%define builddependencies cfitsio/3450-fasrc01  Anaconda/5.0.1-fasrc01
%define rundependencies %{builddependencies}
%define buildcomments %{nil}
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags aci-ref-app-category:Applications;  aci-ref-app-tag:Image analysis
%define apppublication %{nil}


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
rm -rf %{name}_%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}_%{version}_2018Jun22.tar.*
cd %{name}_%{version}
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

%define cfitsiohome ${CFITSIO_HOME}
%define cfitsioinclude ${CFITSIO_INCLUDE}
%define cfitsiolib ${CFITSIO_LIB}
%define builddir ${FASRCSW_DEV}/rpmbuild/BUILD/%{name}_%{version}

export healpixtarget=optimized_gcc
test "%{comp_name}" == "intel" && healpixtarget=linux_icc

test -z $CC && CC=gcc
test -z $FC && FC=gfortran

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}_%{version}

cat > Makefile.patch <<EOF
7,11c7,11
< ALL       = c-void cpp-void f90-void healpy-void
< TESTS     = c-void cpp-void f90-void healpy-void
< CLEAN     = c-void cpp-void f90-void healpy-void
< TIDY      = c-void cpp-void f90-void healpy-void
< DISTCLEAN = c-void cpp-void f90-void healpy-void
---
> ALL       = c-all cpp-all f90-all healpy-all
> TESTS     = c-test cpp-test f90-test healpy-test
> CLEAN     = c-clean cpp-clean f90-clean healpy-clean
> TIDY      = c-tidy cpp-tidy f90-tidy healpy-tidy
> DISTCLEAN = c-distclean cpp-distclean f90-distclean healpy-distclean
16,22c16,22
< HEALPIX=
< F90_BINDIR    =
< F90_INCDIR    =
< F90_LIBDIR    =
< FITSDIR       =
< LIBFITS       =
< F90_BUILDDIR    =
---
> HEALPIX       = %builddir
> F90_BINDIR    = \$(HEALPIX)/bin
> F90_INCDIR    = \$(HEALPIX)/include
> F90_LIBDIR    = \$(HEALPIX)/lib
> FITSDIR       = \${CFITSIO_LIB}
> LIBFITS       = cfitsio
> F90_BUILDDIR  = \$(HEALPIX)/build
24,25c24,25
< F90_FFTSRC  =
< F90_ADDUS   =
---
> F90_FFTSRC    = healpix_fft
> F90_ADDUS     =
29,38c29,38
< F90_FC        =
< F90_FFLAGS    =
< F90_CC        =
< F90_CFLAGS    =
< F90_LDFLAGS   =
< F90_AR      =
< F90_PPFLAGS =
< F90_I8FLAG  =
< F90_LIBSUFFIX =
< F90_FLAGNAMELIB =
---
> F90_FC        = gfortran
> F90_FFLAGS    = -O3 -I\$(F90_INCDIR) -DGFORTRAN -fno-second-underscore -fopenmp -fPIC
> F90_CC        = gcc
> F90_CFLAGS    = -O3 -std=c99 -DgFortran -fopenmp -fPIC
> F90_LDFLAGS   = -L\$(F90_LIBDIR) -L\$(FITSDIR) -lhealpix -lhpxgif -l\$(LIBFITS) -Wl,-R\$(FITSDIR) -lcurl
> F90_AR        = gfortran -fPIC -shared -o
> F90_PPFLAGS   =
> F90_I8FLAG  = -fdefault-integer-8
> F90_LIBSUFFIX = .so
> F90_FLAGNAMELIB = -Wl,-soname,
40,41c40,41
< F90_PGFLAG  =
< F90_PGLIBS  =
---
> F90_PGFLAG  =
> F90_PGLIBS  =
43,44c43,44
< F90_MOD     =
< F90_MODDIR  =
---
> F90_MOD       = mod
> F90_MODDIR    = "-J"
46c46
< F90_OS        =
---
> F90_OS        = Linux
59,61c59,61
< C_CC  =
< C_PIC =
< C_OPT =
---
> C_CC        = gcc
> C_PIC       = -fPIC
> C_OPT       = -O2 -Wall
64,66c64,66
< C_LIBDIR =
< C_INCDIR =
< C_AR     =
---
> C_LIBDIR      = \$(HEALPIX)/lib
> C_INCDIR      = \$(HEALPIX)/include
> C_AR        = ar -rsv
69,73c69,73
< C_WITHOUT_CFITSIO =
< C_CFITSIO_INCDIR =
< C_CFITSIO_LIBDIR =
< C_WLRPATH =
< C_EXTRA_LIB =
---
> C_WITHOUT_CFITSIO = 0
> C_CFITSIO_INCDIR = \${CFITSIO_INCLUDE}
> C_CFITSIO_LIBDIR = \${CFITSIO_LIB}
> C_WLRPATH = -Wl,-R\${CFITSIO_LIB}
> C_EXTRA_LIB = -lcurl
76c76
< C_ALL =
---
> C_ALL     = c-static c-shared
87c87
< HEALPIX_TARGET =
---
> HEALPIX_TARGET = optimized_gcc
89,90c89,90
< CFITSIO_EXT_LIB=
< CFITSIO_EXT_INC=
---
> CFITSIO_EXT_LIB = -L\${CFITSIO_LIB} -lcfitsio -lcurl -Wl,-R\${CFITSIO_LIB}
> CFITSIO_EXT_INC = -I\${CFITSIO_INCLUDE}
95,96c95,96
< HPY_SETUP  =
< HPY_PYTHON =
---
> HPY_SETUP    = setup.py
> HPY_PYTHON   = \${PYTHON_HOME}/bin/python
172a173
> 	export LD_LIBRARY_PATH=\$(HEALPIX)/lib:\${LD_LIBRARY_PATH} ; \\
243a245
> 	export LD_LIBRARY_PATH=\$(HEALPIX)/lib:\${LD_LIBRARY_PATH} ; \\
273a276
> 	export LD_LIBRARY_PATH=\$(HEALPIX)/lib:\${LD_LIBRARY_PATH} ; \\
294a298,299
> 	mkdir -p \$(HEALPIX)/lib/python2.7/site-packages ;\\
> 	export PYTHONPATH=\$(HEALPIX)/lib/python2.7/site-packages:\${PYTHONPATH} ; \\
296c301
< 	\$(HPY_PYTHON) \$(HPY_SETUP) install --user --prefix=; \\
---
> 	\$(HPY_PYTHON) \$(HPY_SETUP) install --prefix=\$(HEALPIX) ; \\
300a306,307
> 	export LD_LIBRARY_PATH=\$(HEALPIX)/lib:\${LD_LIBRARY_PATH} ; \\
> 	export PYTHONPATH=\$(HEALPIX)/lib/python2.7/site-packages:\${PYTHONPATH} ; \\
305a313
> 	export PYTHONPATH=\$(HEALPIX)/lib/python2.7/site-packages:\${PYTHONPATH} ; \\
EOF

patch  --ignore-whitespace -o Makefile Makefile.in Makefile.patch

#Fix screwed up Makefile
#sed -i -e 's?@cp -p libsharp_healpix_f.a $(LIBDIR)/?@cp -p libsharp_healpix_f.a $(LIBDIR)?' src/f90/sharp/Makefile

#Create include, bin, and lib dirs
for d in %builddir/lib %builddir/include %builddir/bin
do
    mkdir -p $d || echo "Directory $d exists"
done

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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}_%{version}
echo %{buildroot} | grep -q %{name}_%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
cp -r {bin,include,lib}  %{buildroot}/%{_prefix}

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
]]
help(helpstr,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}-%{release_short}")
whatis("Description: %{summary_static}")

---- prerequisite apps (uncomment and tweak if necessary)
for i in string.gmatch("%{rundependencies}","%%S+") do 
    if mode()=="load" then
        if not isloaded(i) then
            load(i)
        end
    end
end


---- environment changes (uncomment what is relevant)
setenv("HEALPIX_HOME",              "%{_prefix}")
setenv("HEALPIX_INCLUDE",           "%{_prefix}/include")
setenv("HEALPIX_LIB",               "%{_prefix}/lib")
prepend_path("PATH",                "%{_prefix}/bin")
prepend_path("CPATH",               "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",        "%{_prefix}/lib")
prepend_path("PYTHONPATH",        "%{_prefix}/lib/python2.7/site-packages")
EOF


#------------------- App data file
cat > $FASRCSW_DEV/appdata/%{modulename}.%{type}.dat <<EOF
appname             : %{appname}
appversion          : %{appversion}
description         : %{appdescription}
module              : %{modulename}
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
