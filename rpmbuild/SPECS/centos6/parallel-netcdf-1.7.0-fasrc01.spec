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
%define summary_static PnetCDF is a library providing high-performance parallel I/O while still maintaining file-format compatibility with  Unidata's NetCDF, specifically the formats of CDF-1 and CDF-2.
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/parallel-netcdf-1.7.0.tar.bz2
Source: %{name}-%{version}.tar.bz2

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
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
Parallel netCDF (PnetCDF) is a parallel I/O library that supports data access to NetCDF files in CDF and CDF-2 formats.

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


%define builddependencies %{nil}
%define rundependencies %{builddependencies}
%define buildcomments %{nil}

%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags aci-ref-app-category:Libraries; aci-ref-app-tag:I/O
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

cat <<EOF | patch rules.make
128c128
< 	\$(INSTALL) \$(srcdir)/\$(HEADER) \$@
---
> 	\$(INSTALL) \$(srcdir)/\$(HEADER) \$(DESTDIR)\$@
130c130
< 	\$(INSTALL) \$(srcdir)/\$(HEADER1) \$@
---
> 	\$(INSTALL) \$(srcdir)/\$(HEADER1) \$(DESTDIR)\$@
132c132
< 	\$(INSTALL) \$(srcdir)/\$(HEADER2) \$@
---
> 	\$(INSTALL) \$(srcdir)/\$(HEADER2) \$(DESTDIR)\$@
134c134
< 	\$(INSTALL) \$(srcdir)/\$(HEADER3) \$@
---
> 	\$(INSTALL) \$(srcdir)/\$(HEADER3) \$(DESTDIR)\$@
137,138c137,138
< 	\$(INSTALL) -d -m 755 \$(LIBDIR)
< 	\$(INSTALL) -m 644  \$(LIBRARY) \$@
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(LIBDIR)
> 	\$(INSTALL) -m 644  \$(LIBRARY) \$(DESTDIR)\$@
141,142c141,142
< 	\$(INSTALL) -d -m 755 \$(BINDIR)
< 	\$(INSTALL) -m 755  \$(PROGRAM) \$@
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755  \$(PROGRAM) \$(DESTDIR)\$@
EOF

cat <<EOF | patch man/Makefile.in
46c46
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man3
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man3
51c51
< 	    \$(INSTALL_DATA) \$\$file \$(MANDIR)/man3/\$\$fn \\
---
> 	    \$(INSTALL_DATA) \$\$file \$(DESTDIR)\$(MANDIR)/man3/\$\$fn \\
EOF

cat <<EOF | patch src/lib/Makefile.in
96,101c96,101
< 	\$(INSTALL) -d -m 755 \$(LIBDIR)
< 	\$(INSTALL_DATA) \$(LIBRARY) \$(LIBDIR)/\$(LIBRARY)
< 	\$(INSTALL) -d -m 755 \$(INCDIR)
< 	\$(INSTALL_DATA) \$(HEADER) \$(INCDIR)/\$(HEADER)
< 	\$(INSTALL) -d -m 755 \$(LIBDIR)/pkgconfig
< 	\$(INSTALL_DATA) \$(PKGCONFIG) \$(LIBDIR)/pkgconfig/\$(PKGCONFIG)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(LIBDIR)
> 	\$(INSTALL_DATA) \$(LIBRARY) \$(DESTDIR)\$(LIBDIR)/\$(LIBRARY)
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(INCDIR)
> 	\$(INSTALL_DATA) \$(HEADER) \$(DESTDIR)\$(INCDIR)/\$(HEADER)
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(LIBDIR)/pkgconfig
> 	\$(INSTALL_DATA) \$(PKGCONFIG) \$(DESTDIR)\$(LIBDIR)/pkgconfig/\$(PKGCONFIG)
EOF

cat <<EOF | patch src/libcxx/Makefile.in
75,76c75,76
< 	\$(INSTALL) -d -m 755 \$(INCDIR)
< 	\$(INSTALL_DATA) \$(CXX_HEADER) \$(INCDIR)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(INCDIR)
> 	\$(INSTALL_DATA) \$(CXX_HEADER) \$(DESTDIR)\$(INCDIR)
EOF

cat <<EOF | patch src/libf/Makefile.in
397,398c397,398
< 	\$(INSTALL) -d -m 755 \$(INCDIR)
< 	\$(INSTALL_DATA) pnetcdf.inc \$(INCDIR)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(INCDIR)
> 	\$(INSTALL_DATA) pnetcdf.inc \$(DESTDIR)\$(INCDIR)
EOF

cat <<EOF | patch src/libf90/Makefile.in
77,78c77,78
< 	\$(INSTALL) -d -m 755 \$(INCDIR)
< 	\$(INSTALL_DATA) \$(PNETCDF_MOD) \$(INCDIR)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(INCDIR)
> 	\$(INSTALL_DATA) \$(PNETCDF_MOD) \$(DESTDIR)\$(INCDIR)
EOF

cat <<EOF | patch src/utils/ncmpidiff/Makefile.in
41,42c41,42
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
44,45c44,45
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

cat <<EOF | patch src/utils/ncmpidump/Makefile.in
52,56c52,55
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
< 
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
> 	
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

cat <<EOF | patch src/utils/ncmpigen/Makefile.in
54,55c54,55
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
57,58c57,58
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

cat <<EOF | patch src/utils/ncmpivalid/Makefile.in
43,44c43,44
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
46,47c46,47
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

cat <<EOF | patch src/utils/ncoffsets/Makefile.in
28,31c28,31
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
> 	\$(INSTALL) -d \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

cat <<EOF | patch src/utils/pnetcdf_version/Makefile.in
44,47c44,47
< 	\$(INSTALL) -d -m 755 \$(MANDIR)/man1
< 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(MANDIR)/man1/\$(MANUAL)
< 	\$(INSTALL) -d \$(BINDIR)
< 	\$(INSTALL) -m 755 \$(PROGRAM) \$(BINDIR)/\$(PROGRAM)
---
> 	\$(INSTALL) -d -m 755 \$(DESTDIR)\$(MANDIR)/man1
> 	\$(INSTALL_DATA) \$(srcdir)/\$(MANUAL) \$(DESTDIR)\$(MANDIR)/man1/\$(MANUAL)
> 	\$(INSTALL) -d \$(DESTDIR)\$(BINDIR)
> 	\$(INSTALL) -m 755 \$(PROGRAM) \$(DESTDIR)\$(BINDIR)/\$(PROGRAM)
EOF

./configure MPICC=mpicc MPICXX=mpicxx MPIF77=mpif77 MPIF90=mpif90 --prefix=%{_prefix}

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel

make -j8



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
make install DESTDIR=%{buildroot}

## +++++ START ++++

#
# This app insists on writing directly to the prefix.  Acquiesce, and hack a 
# symlink, IN THE PRODUCTION DESTINATION (yuck), back to our where we want it
# to install in our build environment, and then remove the symlink.  Note that 
# this will only work for the first build of this NAME/VERSION/RELEASE/TYPE 
# combination.
#

# Standard stuff.
# umask 022
# cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
# echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
# mkdir -p %{buildroot}/%{_prefix}

# Make the symlink.
# sudo mkdir -p "$(dirname %{_prefix})"
# test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
# sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"

# make install

# Clean up the symlink.  (The parent dir may be left over, oh well.)
# sudo rm "%{_prefix}"

## +++++ END +++++


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
--if mode()=="load" then
--	if not isloaded("NAME") then
--		load("NAME/VERSION-RELEASE")
--	end
--end

---- environment changes (uncomment what is relevant)
setenv("PNETCDF_HOME",             "%{_prefix}")
setenv("PNETCDF_LIB",              "%{_prefix}/lib")
setenv("PNETCDF_INCLUDE",          "%{_prefix}/include")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/include")
prepend_path("FPATH",              "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("MANPATH",            "%{_prefix}/man")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/lib/pkgconfig")
EOF

#------------------- App data file
cat > $FASRCSW_DEV/appdata/%{modulename}.%{type}.dat <<EOF
---
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
