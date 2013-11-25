Name:       rsync
Version:    3.1.0
Release:    fasrc001
Packager:   Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>
Group:      fasrc

Summary:    FIXME
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


%files

%defattr(-,root,root,-)

#%doc COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS
%doc COPYING README INSTALL NEWS TODO

%{_prefix}/bin/*
#%{_prefix}/sbin/*
#%{_prefix}/lib/*
#%{_prefix}/lib64/*
#%{_prefix}/include/*
#%{_prefix}/man/*
#%{_prefix}/info/*
%{_prefix}/share/*
#%{_prefix}/pkgconfig/*
#%{_prefix}/site-packages/*


%pre


%post


%preun


%postun


%clean
echo %{buildroot} | grep -q 'rpmbuild' && rm -rf %{buildroot}


%changelog
