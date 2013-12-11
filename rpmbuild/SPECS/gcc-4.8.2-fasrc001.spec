Name:       gcc
Version:    4.8.2
Release:    fasrc01
Packager:   Harvard FAS Research Computing -- John Brunelle <john_brunelle@harvard.edu>
Group:      fasrc

Summary:    Various compilers (C, C++, Objective-C, Java, ...)
License:    see COPYING file or upstream packaging

%define GMP_VERSION 5.1.3
%define MPFR_VERSION 3.1.2
%define MPC_VERSION 1.0.1

#https://ftp.gnu.org/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.bz2
Source:     %{name}-%{version}.tar.bz2
#https://ftp.gnu.org/gnu/gmp/gmp-5.1.3.tar.bz2
Source1:    gmp-%{GMP_VERSION}.tar.bz2
#http://www.mpfr.org/mpfr-current/mpfr-3.1.2.tar.bz2
Source2:    mpfr-%{MPFR_VERSION}.tar.bz2
#http://www.multiprecision.org/mpc/download/mpc-1.0.1.tar.gz
Source3:    mpc-%{MPC_VERSION}.tar.gz


#---


%include fasrcsw.rpmmacros

Prefix:     %{_prefix}


%description
The %{name} package contains the GNU Compiler Collection version %{version}.
You'll need this package in order to compile C code.


%prep
%setup -n %{name}-%{version} -q
%setup -n %{name}-%{version} -q -T -D -a 1
%setup -n %{name}-%{version} -q -T -D -a 2
%setup -n %{name}-%{version} -q -T -D -a 3


%build

export LD_LIBRARY_PATH=%{_prefix}/lib:"$LD_LIBRARY_PATH"

#gmp
cd gmp-%{GMP_VERSION}
./configure --prefix=%{_prefix} --enable-cxx
make
make install
cd ..

#mpfr
cd mpfr-%{MPFR_VERSION}
./configure --prefix=%{_prefix} --with-gmp=%{_prefix}
make
make install
cd ..

#mpc
cd mpc-%{MPC_VERSION}
./configure --prefix=%{_prefix} --with-gmp=%{_prefix} --with-mpfr=%{_prefix}
make
make install
cd ..

#gcc
mkdir build
cd build
../configure --prefix=%{_prefix} --enable-languages=c,c++,fortran \
	--with-gmp=%{_prefix} \
	--with-mpfr=%{_prefix} \
	--with-mpc=%{_prefix}
make
cd ..


%install
cd build
make install
cd ..


%files
%defattr(-,root,root,-)
%{_prefix}


%post


%clean
rm -rf %{buildroot}


%changelog
