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
%define summary_static a high-level, high-performance dynamic programming language for technical computing
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL:https://github.com/JuliaLang/julia/releases/download/v0.4.0/julia-0.4.0-full.tar.gz 
# Have to turn this off because a source rpm would be too big (https://bugzilla.redhat.com/show_bug.cgi?id=833427)
# Source: julia-0.4.0-full.tar.gz


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

%define builddependencies cmake/2.8.12.2-fasrc01 git/2.1.0-fasrc01
%define rundependencies %{nil}
%define buildcomments This Julia was built against the general compute processor architecture (JULIA_CPU_TARGET=core2) for Odyssey (i.e. general and interact partitions).  It will not work for login nodes and may not work on many nodes in serial_requeue.
%define requestor Samuel Markson <smarkson@cfa.harvard.edu>
%define requestref RCRT:94396

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags %{nil} 
%define apppublication %{nil}


#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
Julia is a high-level, high-performance dynamic programming language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library. The library, largely written in Julia itself, also integrates mature, best-of-breed C and Fortran libraries for linear algebra, random number generation, signal processing, and string processing. In addition, the Julia developer community is contributing a number of external packages through Julia¿s built-in package manager at a rapid pace. IJulia, a collaboration between the IPython and Julia communities, provides a powerful browser-based graphical notebook interface to Julia.



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
rm -rf %{name}
git clone https://github.com/JuliaLang/julia.git
cd %{name}
git checkout release-0.4 
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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel

#FIXME -- hopefully these openblas issues go away in the future
#out of the box first failed like so:
#	make[5]: Entering directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/deps/openblas-v0.2.10/kernel'
#	../kernel/x86_64/dgemm_kernel_4x4_haswell.S: Assembler messages:
#	../kernel/x86_64/dgemm_kernel_4x4_haswell.S:1398: Error: no such instruction: `vpermpd $ 0xb1,%ymm0,%ymm0'
#	../kernel/x86_64/dgemm_kernel_4x4_haswell.S:1398: Error: no such instruction: `vpermpd $ 0x1b,%ymm0,%ymm0'
#	../kernel/x86_64/dgemm_kernel_4x4_haswell.S:1398: Error: no such instruction: `vpermpd $ 0xb1,%ymm0,%ymm0'
#	...tons of those
#this describes it:
#	https://github.com/JuliaLang/julia/issues/7240
#this workaround:
#	https://github.com/JuliaLang/julia/issues/7240#issuecomment-46168120
#	$ echo 'OPENBLAS_DYNAMIC_ARCH=0' > Make.user
#	but still fails:
#		make[5]: Entering directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/deps/openblas-v0.2.10/kernel'
#		gcc: ../kernel/x86_64/: linker input file unused because linking not done
#		gcc: ../kernel/x86_64/: linker input file unused because linking not done
#		gcc: ../kernel/x86_64/: linker input file unused because linking not done
#		...tons of those
#		ar: sgemm_kernel.o: No such file or directory
#		make[5]: *** [libs] Error 1
#		make[5]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/deps/openblas-v0.2.10/kernel'
#		make[4]: *** [libs] Error 1
#		make[4]: Leaving directory `/odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/deps/openblas-v0.2.10'
#		*** Clean the OpenBLAS build with 'make -C deps clean-openblas'. Rebuild with 'make OPENBLAS_USE_THREAD=0 if OpenBLAS had trouble linking libpthread.so, and with 'make OPENBLAS_TARGET_ARCH=NEHALEM' if there were errors building SandyBridge support. Both these options can also be used simultaneously. ***
#		...
#try the other workaround:
#	https://github.com/JuliaLang/julia/issues/7240#issuecomment-45972436
#	$ echo override USE_SYSTEM_BLAS = 1 >> Make.user
#sed -i -e 's?^OPENBLAS_TARGET_ARCH.*?OPENBLAS_TARGET_ARCH=BULLDOZER?' Make.inc
cat <<EOF > Make.user
USE_SYSTEM_BLAS=1
USE_SYSTEM_LAPACK=1
JULIA_CPU_TARGET=core2
EOF

make %{?_smp_mflags}




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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}


#make these absolute symbolic links relative

#./julia -> /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/usr/bin/julia
rm ./julia
ln -s usr/bin/julia julia

#./usr/share/julia/base -> /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/base
rm ./usr/share/julia/base
ln -s ../../../base ./usr/share/julia/base

#./usr/share/julia/doc -> /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/doc
# rm ./usr/share/julia/doc
# ln -s ../../../doc ./usr/share/julia/doc

#./usr/share/julia/examples -> /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/examples
# rm ./usr/share/julia/examples
# ln -s ../../../examples ./usr/share/julia/examples

#./usr/share/julia/test -> /odyssey/rc_admin/jab/sw/fasrcsw/rpmbuild/BUILD/julia-0.3.0.rc2/test
# rm ./usr/share/julia/test
# ln -s ../../../test ./usr/share/julia/test


#forklift the whole thing, source and all
rsync -av ./ %{buildroot}/%{_prefix}/


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


-- environment changes (uncomment what is relevant)
prepend_path("PATH",                "%{_prefix}/usr/bin")
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
%{_prefix}/.mailmap
%{_prefix}/.git*
%{_prefix}/.travis.yml
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
