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
%define summary_static GTK+, or the GIMP Toolkit, is a multi-platform toolkit for creating graphical user interfaces.
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.31.tar.xz
Source: %{name}+-%{version}.tar.xz

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


## %define builddependencies glib/2.20.4-fasrc01 cairo/1.12.18-fasrc01 pango/1.28.4-fasrc01 atk/1.91.92-fasrc01 pixman/0.20.2-fasrc01 gdk-pixbuf/2.22.1-fasrc01 gobject-introspection/0.10.7-fasrc01
%define builddependencies libffi/3.2.1-fasrc01 python/2.7.13-fasrc01 
%define rundependencies %{builddependencies}
%define buildcomments  Build to use stata-mp on centos6.5
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
GTK+, or the GIMP Toolkit, is a multi-platform toolkit for creating graphical user interfaces.

#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep


#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things -- hopefully it'll just work as-is.
#

umask 022



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

### I actually built this with a script as I did not have time. The script is here
###source new-modules.sh
###module purge
###
####set -e 
###export mysources=/n/home_rc/francesco/helmod/rpmbuild/SOURCES
###export mydest=/n/sw/fasrcsw/apps/Comp/gcc/4.8.2-fasrc01/gtk/2.24.31-fasrc01
###export mytmpdir=/scratch/francesco/GTK
###
###export PATH=${mydest}/bin/:$PATH
###export CPATH=${mydest}/include/:$CPATH
###export INCLUDE=${mydest}/include/:$INCLUDE
###export LIBRARY_PATH=${mydest}/lib/:$LIBRARY_PATH
###export LD_LIBRARY_PATH=${mydest}/lib/:$LD_LIBRARY_PATH
###export PKG_CONFIG_PATH=${mydest}/lib/pkgconfig/:$PKG_CONFIG_PATH
###
###module load libffi/3.2.1-fasrc01 python/2.7.13-fasrc01
###
#####glib
###module load gcc/4.8.2-fasrc01
#####cd $mytmpdir
#####tar xvf ${mysources}/glib-2.54.2.tar.xz 
#####cd glib-2.54.2/
#####./configure --prefix=$mydest --disable-libmount  --with-pcre=internal
#####make -j4 
#####make install 
#####
#######gobject-introspection
#####cd $mytmpdir
#####tar xvf ${mysources}/gobject-introspection-1.54.1.tar.xz 
#####cd gobject-introspection-1.54.1/
#####./configure --prefix=$mydest
#####make -j4
#####make install 
###
#####shared-mime-info
#####cd $mytmpdir
#####tar xvf ${mysources}/shared-mime-info-1.9.tar.xz
#####cd shared-mime-info-1.9
#####./configure --prefix=$mydest
#####make 
#####make install 
#####
#######gdk-pixbuf
#####cd $mytmpdir
#####tar xvf ${mysources}/gdk-pixbuf-2.22.1.tar.gz
#####cd gdk-pixbuf-2.22.1
#####./configure --prefix=$mydest
#####make -j4
#####make install 
###
#####cairo
###module purge
###module load libffi/3.2.1-fasrc01 python/2.7.13-fasrc01
###cd $mytmpdir
###tar xvf ${mysources}/cairo-1.12.18.tar.xz
###cd cairo-1.12.18
###./configure --prefix=$mydest
###make -j4
###make install 
###
#####pango
###module load gcc/4.8.2-fasrc01
###cd $mytmpdir
###tar xvf ${mysources}/pango-1.28.4.tar.gz
###cd pango-1.28.4
###./configure --prefix=$mydest
###make -j4
###make install 
###
#####atk
###cd $mytmpdir
###tar xvf ${mysources}/atk-2.1.92.tar.xz
###cd atk-2.1.92
###./configure --prefix=$mydest
###make -j4
###make install 
###
#####gtk+
###cd $mytmpdir
###tar xvf ${mysources}/gtk+-2.24.31.tar.xz
###cd gtk+-2.24.31
###./configure --prefix=$mydest
###make -j4
###make install 



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
setenv("GTK_HOME",       "%{_prefix}")
prepend_path("PATH",                "%{_prefix}/bin")
prepend_path("CPATH",               "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",        "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib64")
prepend_path("LIBRARY_PATH",        "%{_prefix}/lib64")
prepend_path("PKG_CONFIG_PATH",     "%{_prefix}/lib/pkgconfig")
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
