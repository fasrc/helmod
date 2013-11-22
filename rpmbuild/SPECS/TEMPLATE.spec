Name:       FIXME (e.g. somename)
Version:    FIXME (e.g. 1.2.3)
Release:    FIXME (e.g. fasrc001)
Packager:   Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>
Group:      fasrc

Summary:    FIXME
License:    see COPYING file or upstream packaging

#http://FIXME (put where you got the source here)
Source:     %{name}-%{version}.tar.gz
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

FIXME (remove stuff that is not applicable)

%doc COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS

%{_prefix}/bin/*
%{_prefix}/sbin/*
%{_prefix}/lib/*
%{_prefix}/lib64/*
%{_prefix}/include/*
%{_prefix}/man/*
%{_prefix}/info/*
%{_prefix}/share/*
%{_prefix}/pkgconfig/*
%{_prefix}/site-packages/*


%pre


%post


%preun


%postun


%clean
echo %{buildroot} | grep -q 'rpmbuild' && rm -rf %{buildroot}


%changelog
