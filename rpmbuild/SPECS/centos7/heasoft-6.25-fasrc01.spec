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
%define summary_static HEASOFT is a software suite consisting of the union of FTOOLS/FV, XIMAGE, XRONOS, XSPEC and XSTAR
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://heasarc.gsfc.nasa.gov/FTP/software/lheasoft/release/heasoft-6.25src.tar.gz
#XSPEC Patch: https://heasarc.gsfc.nasa.gov/docs/xanadu/xspec/issues/Xspatch_121001b.tar.gz
#Patcher: https://heasarc.gsfc.nasa.gov/docs/xanadu/xspec/issues/patch_install_4.10.tcl
Source: %{name}-%{version}src.tar.gz

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


%define builddependencies %{nil}
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
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
HEASOFT is a software suite consisting of the union of FTOOLS/FV, XIMAGE, XRONOS, XSPEC and XSTAR.


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
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}src.tar.*
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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/BUILD_DIR

cd ../Xspec/src/
cp "$FASRCSW_DEV"/rpmbuild/SOURCES/Xspatch_121001b.tar.gz .
tclsh patch_install_4.10.tcl -no_build

cd ../../BUILD_DIR

./configure --prefix=%{_prefix}

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel
make



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

#umask 022
#cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/BUILD_DIR
#echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
#mkdir -p %{buildroot}/%{_prefix}
#make install DESTDIR=%{buildroot}

# Standard stuff.
umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/BUILD_DIR
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

# Make the symlink.
sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"

make install

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
setenv("HEASOFT_HOME",       "%{_prefix}")
setenv("XANBIN",                   "%{_prefix}/x86_64-pc-linux-gnu-libc2.17")
setenv("LHEAPERL",                 "/usr/bin/perl")
setenv("TCLRL_LIBDIR",             "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib")
setenv("POW_LIBRARY",              "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/pow")
setenv("PGPLOT_DIR",               "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib")
setenv("PGPLOT_RGB",               "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/rgb.txt")
setenv("PGPLOT_FONT",              "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/grfont.dat")
setenv("FTOOLS",                   "%{_prefix}/x86_64-pc-linux-gnu-libc2.17")
setenv("HEADAS",                   "%{_prefix}/x86_64-pc-linux-gnu-libc2.17")
setenv("PFILES",                   "/scratch;%{_prefix}/x86_64-pc-linux-gnu-libc2.17/syspfiles")
setenv("LHEASOFT",                 "%{_prefix}/x86_64-pc-linux-gnu-libc2.17")
setenv("LHEA_HELP",                "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/help")
setenv("LHEA_DATA",                "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/refdata")
setenv("XRDEFAULTS",               "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/xrdefaults")
setenv("XANADU",                   "%{_prefix}")
prepend_path("PERL5LIB",           "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/perl")
prepend_path("PERLLIB",            "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/perl")
prepend_path("PATH",               "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/attitude/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/heasptools/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/heatools/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/heagen/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/demo/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/suzaku/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/swift/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/Xspec/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/integral/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/maxi/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/nicer/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/nustar/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/hitomi/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/ftools/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/heasim/x86_64-pc-linux-gnu-libc2.17/bin")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/attitude/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/heagen/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/suzaku/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/swift/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/Xspec/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/integral/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/maxi/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/nustar/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/hitomi/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("CPATH",              "%{_prefix}/ftools/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/attitude/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/heagen/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/suzaku/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/swift/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/Xspec/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/integral/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/maxi/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/nustar/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/hitomi/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("FPATH",              "%{_prefix}/ftools/x86_64-pc-linux-gnu-libc2.17/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/attitude/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/heagen/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/demo/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/suzaku/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/swift/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/Xspec/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/maxi/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/nicer/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/nustar/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/hitomi/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ftools/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/attitude/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/heagen/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/demo/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/suzaku/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/swift/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/Xspec/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/maxi/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/nicer/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/nustar/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/hitomi/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ftools/x86_64-pc-linux-gnu-libc2.17/lib")
prepend_path("MANPATH",            "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/share/man")
prepend_path("MANPATH",            "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/share/man")
prepend_path("MANPATH",            "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/man")
prepend_path("MANPATH",            "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/man")
prepend_path("MANPATH",            "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/share/man")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/heacore/x86_64-pc-linux-gnu-libc2.17/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/x86_64-pc-linux-gnu-libc2.17/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/tcltk/x86_64-pc-linux-gnu-libc2.17/lib/pkgconfig")
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
