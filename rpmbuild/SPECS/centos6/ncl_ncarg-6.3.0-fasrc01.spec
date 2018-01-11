# The spec involves the hack that allows the app to write directly to the 
# production location.  The following allows the production location path to be 
# used in files that the rpm builds.
%define __arch_install_post %{nil}

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
%define summary_static NCL, a product of the Computational & Information Systems Laboratory at the National Center for Atmospheric Research (NCAR) and sponsored by the National Science Foundation, is a free interpreted language designed specifically for scientific data processing and visualization. 
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://www.earthsystemgrid.org/download/fileDownload.html?logicalFileId=bec58cb3-cd9b-11e4-bb80-00c0f03d5b7c
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



%define builddependencies proj/4.8.0-fasrc01 libpng/1.5.21-fasrc01 zlib/1.2.8-fasrc04 gdal/1.11.1-fasrc02 g2lib/1.4.0-fasrc01 g2clib/1.4.0-fasrc01 netcdf/4.3.3.1-fasrc02 vis5d+/1.3.0-fasrc04 udunits/2.2.18-fasrc01 cairo/1.12.18-fasrc01 jasper/1.900.1-fasrc01 szip/2.1-fasrc01 jpeg/6b-fasrc01 
%define rundependencies %{builddependencies}
%define buildcomments Built for Packard Chan
%define requestor Packard Chan <packard.chan@gmail.com>
%define requestref RCRT:102320

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
NCL has robust file input and output. It can read and write netCDF-3, netCDF-4 classic, netCDF-4, HDF4, binary, and ASCII data. It can read HDF-EOS2, HDF-EOS5, GRIB1, GRIB2, and OGR files (shapefiles, MapInfo, GMT, Tiger). It can be built as an OPeNDAP client.
NCL visualizations are world class and highly customizable.



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

%define libsearch -L$ZLIB_LIB -L$LIBPNG_LIB -L$SZIP_LIB -L$VIS5D_LIB -L$GDAL_LIB -L$PROJ_LIB -L$UDUNITS_LIB -L$NETCDF_LIB -L$G2LIB_LIB -L$G2CLIB_LIB -L$CAIRO_LIB -L$JASPER_LIB -L$JPEG_LIB -L/usr/lib64 -L/usr/lib
%define incsearch -I$ZLIB_INCLUDE -I$LIBPNG_INCLUDE -I$SZIP_INCLUDE -I$VIS5D_INCLUDE -I$GDAL_INCLUDE -I$PROJ_INCLUDE -I$UDUNITS_INCLUDE -I$NETCDF_INCLUDE -I$G2CLIB_INCLUDE -I$CAIRO_INCLUDE -I$JASPER_INCLUDE -I$JPEG_INCLUDE -I/usr/include/freetype2 -I/usr/include

cat <<EOF > config/Site.local
#ifdef FirstSite

#endif /* FirstSite */


#ifdef SecondSite

#define YmakeRoot %{_prefix}

#define HDFlib -ldf -ljpeg -lz -lsz -lgrib2c -ljasper

#define LibSearch %{libsearch}

#define IncSearch %{incsearch}

#define BuildGDAL 1
#define BuildTRIANGLE 0
#define BuildGRIB2 1
#define GRIB2lib
#define BuildV5D 1

#define NoMakeDepend

#endif /* SecondSite */

EOF

./Configure -v

#sed -i -e 's?PartialLibraryTarget(libncarg_gks.a,$(OBJECTS))?PartialLibraryTarget(libncarg_gks.a,$(OBJECTS) $(ROBJ_OBJ))?'  ncarg2d/src/libncarg_gks/awi/yMakefile

#make Makefiles
#sed -i -e 's?^../libncarg_gks.a:: $(OBJECTS)?../libncarg_gks.a:: $(OBJECTS) $(ROBJ_OBJ)?' \
#       -e 's?$(AR_REG) ../libncarg_gks.a $(OBJECTS)?$(AR_REG) ../libncarg_gks.a $(OBJECTS) $(ROBJ_OBJ)?' ncarg2d/src/libncarg_gks/awi/Makefile
   

make Build
rm ncarg2d/src/libncarg_gks/awi/ggkwdr_stub.o

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel



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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"

make Everything

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
setenv("NCL_NCARG_HOME",           "%{_prefix}")
setenv("NCL_NCARG_LIB",            "%{_prefix}/lib")
setenv("NCL_NCARG_INCLUDE",        "%{_prefix}/include")
prepend_path("PATH",               "%{_prefix}/lib/ncarg/data/bin")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/include")
prepend_path("FPATH",              "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("MANPATH",            "%{_prefix}/man")
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
