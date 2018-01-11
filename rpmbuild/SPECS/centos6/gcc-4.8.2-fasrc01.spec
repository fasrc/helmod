#------------------- package info ----------------------------------------------

#
# FIXME
#
# enter the simple app name, e.g. myapp
#
Name: gcc

#
# FIXME
#
# enter the app version, e.g. 0.0.1
#
Version: 4.8.2

#
# FIXME
#
# enter the base release; start with fasrc01 and increment in subsequent 
# releases; the actual "Release" is constructed dynamically and set below
#
%define release_short fasrc01

#
# FIXME
#
# enter your FIRST LAST <EMAIL>
#
Packager: Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>

#
# FIXME
#
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo 
# rpm gets created, so this stores it separately for later re-use)
#
%define summary_static the GNU Compiler Collection
Summary: %{summary_static}

#
# FIXME
#
# enter the url from where you got the source, as a comment; change the archive 
# suffix if applicable
#
#https://ftp.gnu.org/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.bz2
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


%define builddependencies gmp/5.1.3-fasrc01 mpfr/3.1.2-fasrc01 mpc/1.0.1-fasrc01 
%define rundependencies %{builddependencies}
%define buildcomments %{nil}
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags %{nil} 
%define apppublication %{nil}


#
# FIXME
#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
The GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Java, Ada, and Go, as well as libraries for these languages (libstdc++, libgcj,...). GCC was originally written as the compiler for the GNU operating system. The GNU system was developed to be 100% free software, free in the sense that it respects the user's freedom.



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

%setup



#------------------- %%build (~ configure && make) ----------------------------

%build

#
# FIXME
#
# configure and make the software here; the default below is for standard 
# GNU-toolchain style things
# 

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

#prerequisite apps (uncomment and tweak if necessary)
#keep these synced with the %%install section!
#this is from the default %%configure macro + make, except remove -m64, work in a separate objdir subdirectory, and use parallel make
CFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
export CFLAGS
CXXFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
export CXXFLAGS
FFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
export FFLAGS

cd %{_topdir}/BUILD/%{name}-%{version}
mkdir objdir
cd objdir
../configure \
  --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu \
  --program-prefix= \
  --prefix=%{_prefix} \
  --exec-prefix=%{_prefix} \
  --bindir=%{_prefix}/bin \
  --sbindir=%{_prefix}/sbin \
  --sysconfdir=%{_prefix}/etc \
  --datadir=%{_prefix}/share \
  --includedir=%{_prefix}/include \
  --libdir=%{_prefix}/lib64 \
  --libexecdir=%{_prefix}/libexec \
  --localstatedir=%{_prefix}/var \
  --sharedstatedir=%{_prefix}/var/lib \
  --mandir=%{_prefix}/share/man \
  --infodir=%{_prefix}/share/inf
make %{?_smp_mflags}
cd ..



#------------------- %%install (~ make install + create modulefile) -----------

%install

#
# FIXME
#
# make install here; the default below is for standard GNU-toolchain style 
# things; plus we add some handy files (if applicable) and build a modulefile
#

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#this is from the default %%makeinstall macro, except load modules and work in a separate objdir subdirectory
cd %{_topdir}/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}
cd objdir
make install DESTDIR=%{buildroot}
cd ..

#these files are nice to have; %%doc is not as prefix-friendly as I would like
#if there are other files not installed by make install, add them here
for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	test -e "$f" && ! test -e '%{buildroot}/%{_prefix}/'"$f" && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

#this is the part that allows for inspecting the build output without fully creating the rpm
#there should be no need to change this
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
# - uncomment any applicable prepend_path things
#
# - do any other customizing of the module, e.g. load dependencies
#
# - in the help message, link to website docs rather than write anything 
#   lengthy here
#
# references on writing modules:
#   http://www.tacc.utexas.edu/tacc-projects/lmod/advanced-user-guide/writing-module-files
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/initial-setup-of-modules
#   http://www.tacc.utexas.edu/tacc-projects/lmod/system-administrator-guide/module-commands-tutorial
#
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
        load(i)
    end
end


---- environment changes (uncomment what is relevant)

setenv("CC" , "gcc")
setenv("CXX", "g++")
setenv("FC" , "gfortran")
setenv("F77", "gfortran")

prepend_path("PATH",              "%{_prefix}/bin")
prepend_path("LD_LIBRARY_PATH",   "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",   "%{_prefix}/lib64")
prepend_path("LIBRARY_PATH",      "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",      "%{_prefix}/lib64")
prepend_path("PKG_CONFIG_PATH",   "%{_prefix}/lib64/pkgconfig")
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/include")
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/install-tools/include")
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/plugin/include")
prepend_path("CPATH",             "%{_prefix}/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/install-tools/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.8.2/plugin/include")
prepend_path("FPATH",             "%{_prefix}/include")
prepend_path("MANPATH",           "%{_prefix}/share/man")

local mroot = os.getenv("MODULEPATH_ROOT")
local mdir = pathJoin(mroot, "Comp/%{name}/%{version}-%{release_short}")
prepend_path("MODULEPATH", mdir)
setenv("FASRCSW_COMP_NAME"   , "%{name}")
setenv("FASRCSW_COMP_VERSION", "%{version}")
setenv("FASRCSW_COMP_RELEASE", "%{release_short}")
family("Comp")
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
