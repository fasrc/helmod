#
# This is failing to build
#

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
# rpm gets created, so this stores it separately for later re-use)
#
%define summary_static the GNU Compiler Collection
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://ftp.gnu.org/gnu/gcc/gcc-4.9.0/gcc-4.9.0.tar.bz2
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
%description
The GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Java, Ada, and Go, as well as libraries for these languages (libstdc++, libgcj,...). GCC was originally written as the compiler for the GNU operating system. The GNU system was developed to be 100% free software, free in the sense that it respects the user's freedom.



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

%setup



#------------------- %%build (~ configure && make) ----------------------------

%build

#
# configure and make the software here; the default below is for standard 
# GNU-toolchain style things
# 

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

##prerequisite apps (uncomment and tweak if necessary)
module load gmp/6.0.0-fasrc01
module load mpfr/3.1.2-fasrc02
module load mpc/1.0.2-fasrc01

#this is from the default %%configure macro + make, except:
#	work in a separate objdir subdirectory
#	remove -m64; otherwise get:
#		# @multilib_flags@ is still needed because this may use
#		# /n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/host-x86_64-redhat-linux-gnu/gcc/xgcc -B/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/host-x86_64-redhat-linux-gnu/gcc/ -B/n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/bin/ -B/n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/lib/ -isystem /n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/include -isystem /n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/sys-include    and -O2  -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -DIN_GCC   -W -Wall -Wwrite-strings -Wcast-qual -Wstrict-prototypes -Wmissing-prototypes -Wold-style-definition  -isystem ./include   -fpic -mlong-double-80 -g -DIN_LIBGCC2 -fbuilding-libgcc -fno-stack-protector  directly.
#		# @multilib_dir@ is not really necessary, but sometimes it has
#		# more uses than just a directory name.
#		/bin/sh ../../.././libgcc/../mkinstalldirs 32
#		mkdir -p -- 32
#		/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/host-x86_64-redhat-linux-gnu/gcc/xgcc -B/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/host-x86_64-redhat-linux-gnu/gcc/ -B/n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/bin/ -B/n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/lib/ -isystem /n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/include -isystem /n/sw/fasrcsw/apps/Core/gcc/4.8.2-fasrc01/x86_64-redhat-linux-gnu/sys-include    -O2  -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -DIN_GCC   -W -Wall -Wwrite-strings -Wcast-qual -Wstrict-prototypes -Wmissing-prototypes -Wold-style-definition  -isystem ./include   -fpic -mlong-double-80 -g -DIN_LIBGCC2 -fbuilding-libgcc -fno-stack-protector  -shared -nodefaultlibs -Wl,--soname=libgcc_s.so.1 -Wl,--version-script=libgcc.map -o 32/libgcc_s.so.1.tmp -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -m32 -B./ _muldi3_s.o _negdi2_s.o _lshrdi3_s.o _ashldi3_s.o _ashrdi3_s.o _cmpdi2_s.o _ucmpdi2_s.o _clear_cache_s.o _trampoline_s.o __main_s.o _absvsi2_s.o _absvdi2_s.o _addvsi3_s.o _addvdi3_s.o _subvsi3_s.o _subvdi3_s.o _mulvsi3_s.o _mulvdi3_s.o _negvsi2_s.o _negvdi2_s.o _ctors_s.o _ffssi2_s.o _ffsdi2_s.o _clz_s.o _clzsi2_s.o _clzdi2_s.o _ctzsi2_s.o _ctzdi2_s.o _popcount_tab_s.o _popcountsi2_s.o _popcountdi2_s.o _paritysi2_s.o _paritydi2_s.o _powisf2_s.o _powidf2_s.o _powixf2_s.o _powitf2_s.o _mulsc3_s.o _muldc3_s.o _mulxc3_s.o _multc3_s.o _divsc3_s.o _divdc3_s.o _divxc3_s.o _divtc3_s.o _bswapsi2_s.o _bswapdi2_s.o _clrsbsi2_s.o _clrsbdi2_s.o _fixunssfsi_s.o _fixunsdfsi_s.o _fixunsxfsi_s.o _fixsfdi_s.o _fixdfdi_s.o _fixxfdi_s.o _fixunssfdi_s.o _fixunsdfdi_s.o _fixunsxfdi_s.o _floatdisf_s.o _floatdidf_s.o _floatdixf_s.o _floatundisf_s.o _floatundidf_s.o _floatundixf_s.o _divdi3_s.o _moddi3_s.o _udivdi3_s.o _umoddi3_s.o _udiv_w_sdiv_s.o _udivmoddi4_s.o cpuinfo_s.o tf-signs_s.o sfp-exceptions_s.o addtf3_s.o divtf3_s.o eqtf2_s.o getf2_s.o letf2_s.o multf3_s.o negtf2_s.o subtf3_s.o unordtf2_s.o fixtfsi_s.o fixunstfsi_s.o floatsitf_s.o floatunsitf_s.o fixtfdi_s.o fixunstfdi_s.o floatditf_s.o floatunditf_s.o extendsftf2_s.o extenddftf2_s.o extendxftf2_s.o trunctfsf2_s.o trunctfdf2_s.o trunctfxf2_s.o enable-execute-stack_s.o unwind-dw2_s.o unwind-dw2-fde-dip_s.o unwind-sjlj_s.o unwind-c_s.o emutls_s.o libgcc.a -lc && rm -f 32/libgcc_s.so && if [ -f 32/libgcc_s.so.1 ]; then mv -f 32/libgcc_s.so.1 32/libgcc_s.so.1.backup; else true; fi && mv 32/libgcc_s.so.1.tmp 32/libgcc_s.so.1 && ln -s libgcc_s.so.1 32/libgcc_s.so
#		/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/host-x86_64-redhat-linux-gnu/gcc/32/crtbeginS.o: could not read symbols: File in wrong format
#		collect2: error: ld returned 1 exit status
#		make[5]: *** [libgcc_s.so] Error 1
#		make[5]: Leaving directory `/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/x86_64-redhat-linux-gnu/32/libgcc'
#		make[4]: *** [multi-do] Error 1
#		make[4]: Leaving directory `/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/x86_64-redhat-linux-gnu/libgcc'
#		make[3]: *** [all-multi] Error 2
#		make[3]: Leaving directory `/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2/x86_64-redhat-linux-gnu/libgcc'
#		make[2]: *** [all-stage1-target-libgcc] Error 2
#		make[2]: Leaving directory `/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2'
#		make[1]: *** [stage1-bubble] Error 2
#		make[1]: Leaving directory `/n/home_rc/jab/harvard/sw/fasrcsw/rpmbuild/BUILD/gcc-4.8.2'
#		make: *** [all] Error 2
#		error: Bad exit status from /var/tmp/rpm-tmp.s2JhGQ (%%build)
#	remove -Wp,-D_FORTIFY_SOURCE=2; otherwise get:
#		libtool: compile:  /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/./gcc/xgcc -shared-libgcc -B/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/./gcc -nostdinc++ -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/src -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/src/.libs -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/libsupc++/.libs -B/n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/bin/ -B/n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/lib/ -isystem /n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/include -isystem /n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/sys-include -D_GNU_SOURCE -D_DEBUG -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -I. -I../../../../libsanitizer/sanitizer_common -I.. -I ../../../../libsanitizer/include -isystem ../../../../libsanitizer/include/system -Wall -W -Wno-unused-parameter -Wwrite-strings -pedantic -Wno-long-long -fPIC -fno-builtin -fno-exceptions -fno-rtti -fomit-frame-pointer -funwind-tables -fvisibility=hidden -Wno-variadic-macros -I../../libstdc++-v3/include -I../../libstdc++-v3/include/x86_64-redhat-linux-gnu -I../../../../libsanitizer/../libstdc++-v3/libsupc++ -DSANITIZER_LIBBACKTRACE -DSANITIZER_CP_DEMANGLE -I ../../../../libsanitizer/../libbacktrace -I ../libbacktrace -I ../../../../libsanitizer/../include -include ../../../../libsanitizer/libbacktrace/backtrace-rename.h -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic -D_GNU_SOURCE -MT sanitizer_platform_limits_posix.lo -MD -MP -MF .deps/sanitizer_platform_limits_posix.Tpo -c ../../../../libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc  -fPIC -DPIC -o .libs/sanitizer_platform_limits_posix.o
#		In file included from /usr/include/mqueue.h:96:0,
#						 from ../../../../libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc:72:
#		/usr/include/bits/mqueue2.h: In function 'mqd_t mq_open(const char*, int, ...)':
#		/usr/include/bits/mqueue2.h:37:48: error: declaration of 'mqd_t mq_open(const char*, int, ...)' has a different exception specifier
#		 mq_open (__const char *__name, int __oflag, ...)
#														^
#		/usr/include/bits/mqueue2.h:26:14: error: from previous declaration 'mqd_t mq_open(const char*, int, ...) throw ()'
#		 extern mqd_t mq_open (__const char *__name, int __oflag, ...)
#					  ^
#		make[5]: *** [sanitizer_platform_limits_posix.lo] Error 1
#		make[5]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libsanitizer/sanitizer_common'
#		make[4]: *** [all-recursive] Error 1
#		make[4]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libsanitizer'
#		make[3]: *** [all] Error 2
#		make[3]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libsanitizer'
#		make[2]: *** [all-target-libsanitizer] Error 2
#		make[2]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir'
#		make[1]: *** [all] Error 2
#		make[1]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir'
#		error: Bad exit status from /var/tmp/rpm-tmp.jXotXt (%%build)
#   but still failing:
#		libtool: compile:  /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/./gcc/xgcc -shared-libgcc -B/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/./gcc -nostdinc++ -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/src -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/src/.libs -L/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/gcc-4.9.0/objdir/x86_64-redhat-linux-gnu/libstdc++-v3/libsupc++/.libs -B/n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/bin/ -B/n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/lib/ -isystem /n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/include -isystem /n/sw/fasrcsw/apps/Core/gcc/4.9.0-fasrc01/x86_64-redhat-linux-gnu/sys-include -D_GNU_SOURCE -D_DEBUG -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -I. -I../../../../libsanitizer/sanitizer_common -I.. -I ../../../../libsanitizer/include -isystem ../../../../libsanitizer/include/system -Wall -W -Wno-unused-parameter -Wwrite-strings -pedantic -Wno-long-long -fPIC -fno-builtin -fno-exceptions -fno-rtti -fomit-frame-pointer -funwind-tables -fvisibility=hidden -Wno-variadic-macros -I../../libstdc++-v3/include -I../../libstdc++-v3/include/x86_64-redhat-linux-gnu -I../../../../libsanitizer/../libstdc++-v3/libsupc++ -DSANITIZER_LIBBACKTRACE -DSANITIZER_CP_DEMANGLE -I ../../../../libsanitizer/../libbacktrace -I ../libbacktrace -I ../../../../libsanitizer/../include -include ../../../../libsanitizer/libbacktrace/backtrace-rename.h -O2 -g -pipe -Wall -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic -D_GNU_SOURCE -MT sanitizer_symbolizer_libbacktrace.lo -MD -MP -MF .deps/sanitizer_symbolizer_libbacktrace.Tpo -c ../../../../libsanitizer/sanitizer_common/sanitizer_symbolizer_libbacktrace.cc  -fPIC -DPIC -o .libs/sanitizer_symbolizer_libbacktrace.o
#		In file included from ../../../../libsanitizer/../include/libiberty.h:43:0,
#						 from ../../../../libsanitizer/../include/demangle.h:33,
#						 from ../../../../libsanitizer/sanitizer_common/sanitizer_symbolizer_libbacktrace.cc:25:
#		../../../../libsanitizer/../include/ansidecl.h:171:64: error: declaration of 'int asprintf(char**, const char*, ...)' has a different exception specifier
#		 #  define ATTRIBUTE_NONNULL(m) __attribute__ ((__nonnull__ (m)))
#	so take these out:
#		CFLAGS='-O2 -g -pipe -Wall -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
#		export CFLAGS
#		CXXFLAGS='-O2 -g -pipe -Wall -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
#		export CXXFLAGS
#		FFLAGS='-O2 -g -pipe -Wall -fexceptions -fstack-protector --param=ssp-buffer-size=4 -mtune=generic'
#		export FFLAGS
#
#		--build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu \
cd %{_topdir}/BUILD/%{name}-%{version}
mkdir objdir
cd objdir
../configure \
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
make
cd ..



#------------------- %%install (~ make install + create modulefile) -----------

%install

#
# make install here; the default below is for standard GNU-toolchain style 
# things; plus we add some handy files (if applicable) and build a modulefile
#

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

#(sorta oddly, install will fail if the shared libs are not available)
module load gmp/6.0.0-fasrc01
module load mpfr/3.1.2-fasrc02
module load mpc/1.0.2-fasrc01

#this is from the default %%make_install macro, except load modules and work in a separate objdir subdirectory
cd %{_topdir}/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
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

# FIXME (but the above is enough for a "trial" build)

cat > %{buildroot}/%{_prefix}/modulefile.lua <<EOF
local helpstr = [[
%{name}-%{version}-%{release_short}
%{summary_static}
]]
help(helpstr,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}-%{release_short}")
whatis("Description: %{summary_static}")

-- prerequisite apps (uncomment and tweak if necessary)
if mode()=="load" then
	if not isloaded("gmp") then
		load("gmp/6.0.0-fasrc01")
	end
	if not isloaded("mpfr") then
		load("mpfr/3.1.2-fasrc02")
	end
	if not isloaded("mpc") then
		load("mpc/1.0.2-fasrc01")
	end
end

---- environment changes (uncomment what's relevant)

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
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/include")
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/install-tools/include")
prepend_path("CPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/plugin/include")
prepend_path("CPATH",             "%{_prefix}/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/install-tools/include")
prepend_path("FPATH",             "%{_prefix}/lib64/gcc/x86_64-redhat-linux-gnu/4.9.0/plugin/include")
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
