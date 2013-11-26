Name:       rsync
Version:    3.1.0
Release:    fasrc001
Packager:   Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>
Group:      fasrc

#%{summary} gets changed when the debuginfo rpm gets created, so store the original for later re-use
%define     summary_static FIXME
Summary:    %{summary_static}

License:    see COPYING file or upstream packaging

#http://rsync.samba.org/ftp/rsync/rsync-3.1.0.tar.gz
Source:     %{name}-%{version}.tar.gz


#---


%include fasrcsw.rpmmacros

Prefix:     %{_prefix}


%description
FIXME


%prep

%setup -q


%build

%configure
make


%install

%makeinstall

cat > %{buildroot}/%{_prefix}/modulefile <<EOF
local help_message = [[
%{name}-%{version}-%{release}

%{summary_static}
]]
help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: compiler")
whatis("Keywords: system, compiler")

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

#%doc COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS
%doc COPYING README INSTALL NEWS TODO

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

%{_prefix}/modulefile


%pre

mkdir -p %{_prefix}


%post

mkdir -p %{modulefile_dir}
ln -s %{_prefix}/modulefile %{modulefile}


%preun

rm %{modulefile}
##do not do this, it would remove the entire app's directory
#rmdir %{modulefile_dir}


%postun

#(JAB doesn't understand share/doc -- if JAB adds it to %files, rpmbuild gives an an EEXIST, even though it exists)
rmdir %{_prefix}/share/doc
rmdir %{_prefix}/share
rmdir %{_prefix}


%clean
echo %{buildroot} | grep -q 'rpmbuild' && rm -rf %{buildroot}


%changelog
