#
# FIXME
# enter the simple app name
#
Name: rsync

#
# FIXME
# enter the app version
#
Version: 3.1.0

#
# FIXME
# enter the app release; start with fasrc01 and increment in subsequent 
# releases
#
Release: fasrc01

#
# FIXME
# enter your FIRST, LAST, and EMAIL
#
Packager: Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>

#
# FIXME
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo 
# rpm gets created, so this stores it separately for later re-use)
#
%define summary_static A program for synchronizing files over a network
Summary: %{summary_static}

#
# FIXME
# enter the url from where you got the source, as a comment; change the archive 
# suffix if applicable
#
#http://rsync.samba.org/ftp/rsync/rsync-3.1.0.tar.gz
Source:     %{name}-%{version}.tar.gz

#(these fields are required)
Group: fasrcsw
License: see COPYING file or upstream packaging

%include fasrcsw.rpmmacros

Prefix:     %{_prefix}


#
# FIXME
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.


%prep

%setup -q


%build

%configure
make


%install

%makeinstall

#(these files are nice to have; %%doc is not as prefix-friendly as I would like)
for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	[ -e "$f" ] && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

#
# FIXME
# consider uncommenting this on the first trial rpmbuild to see what the 
# package actually builds, so you can choose what to include in %%files, the 
# modulefile, etc. below
# 
#echo
#echo
#tree '%{buildroot}/%{_prefix}'
#false

# 
# FIXME
#
# - uncomment any applicable prepend_path things and mirror what you do here in 
#   the %%files section below
#
# - do any other customizing of the module
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
%{name}-%{version}-%{release}
%{summary_static}
]]
help(helpstr,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}-%{release}")
whatis("Description: %{summary_static}")

prepend_path("PATH",                "%{_prefix}/bin")
--prepend_path("PATH",                "%{_prefix}/sbin")
--prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib")
--prepend_path("LIBRARY_PATH",        "%{_prefix}/lib")
--prepend_path("LD_LIBRARY_PATH",     "%{_prefix}/lib64")
--prepend_path("LIBRARY_PATH",        "%{_prefix}/lib64")
--prepend_path("CPATH",               "%{_prefix}/include")
--prepend_path("FPATH",               "%{_prefix}/include")
--prepend_path("MANPATH",             "%{_prefix}/man")
--prepend_path("INFOPATH",            "%{_prefix}/info")
prepend_path("MANPATH",             "%{_prefix}/share/man")
--prepend_path("PKG_CONFIG_PATH",     "%{_prefix}/pkgconfig")
--prepend_path("PYTHONPATH",          "%{_prefix}/site-packages")
EOF


%files

%defattr(-,root,root,-)

#
# FIXME
# uncomment anything applicable here (if anything gets added to the template, 
# add it in the %%install section above, too)
#
%{_prefix}/COPYING
#%{_prefix}/AUTHORS
%{_prefix}/README
%{_prefix}/INSTALL
#%{_prefix}/ChangeLog
%{_prefix}/NEWS
#%{_prefix}/THANKS
%{_prefix}/TODO
#%{_prefix}/BUGS

#
# FIXME
# uncomment anything applicable here; keep this in sync with the modulefile above
#
%{_prefix}/bin
#%{_prefix}/sbin
#%{_prefix}/lib
#%{_prefix}/lib64
#%{_prefix}/include
#%{_prefix}/man
#%{_prefix}/info
%{_prefix}/share
#%{_prefix}/pkgconfig
#%{_prefix}/site-packages

%{_prefix}/modulefile.lua


%pre
#
# everything in fasrcsw is installed in an app hierarchy in which some 
# components may need creating, but no single rpm should own them, since parts 
# are shared; only do this if it looks like an app-specific prefix is indeed 
# being used (that's the fasrcsw default)
#
echo '%{_prefix}' | grep -q '%{name}.%{version}.%{release}' && mkdir -p '%{_prefix}'
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
test -d '%{_prefix}' && echo '%{_prefix}' | grep -q '%{name}.%{version}.%{release}' && rmdir '%{_prefix}'
#


%clean
#
# wipe out the buildroot, but put some protection to make sure it isn't 
# accidentally / or something -- we always have "rpmbuild" in the name
#
echo '%{buildroot}' | grep -q 'rpmbuild' && rm -rf '%{buildroot}'
#


%changelog
#
# FIXME
# if you're issuing a new fasrc### release, explain the changes
#
