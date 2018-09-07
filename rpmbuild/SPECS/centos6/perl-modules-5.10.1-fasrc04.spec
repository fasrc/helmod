#------------------- package info ----------------------------------------------
#
# For this to work, cpanm (CPAN Minus) must be installed
#

#
# FIXME
#
# enter the simple app name, e.g. myapp
#
Name: perl-modules

#
# FIXME
#
# enter the app version, e.g. 0.0.1
#
Version: 5.10.1

#
# FIXME
#
# enter the base release; start with fasrc01 and increment in subsequent 
# releases; the actual "Release" is constructed dynamically and set below
#
%define release_short %{getenv:RELEASE}

#
# FIXME
#
# enter your FIRST LAST <EMAIL>
#
Packager: Harvard FAS Research Computing -- Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>

#
# FIXME
#
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo 
# rpm gets created, so this stores it separately for later re-use)
#
%define summary_static A module that represents a large list of individual Perl modules
Summary: %{summary_static}

#
# FIXME
#
# enter the url from where you got the source, as a comment; change the archive 
# suffix if applicable
#
#http://...FIXME...
Source: %{name}-%{version}.tar.gz

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


%define builddependencies  perl/5.10.1-fasrc01 gd/2.0.28-fasrc01
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
# The list of modules installed via cpan
#
%define MODULES ExtUtils-MakeMaker-6.98 IO-String-1.08 Test-Deep-0.112 Tree-DAG_Node-1.20 Test-Warn-0.24 Class-Data-Inheritable-0.08 Algorithm-Diff-1.1902 Scalar-List-Utils-1.38 Parse-CPAN-Meta-1.4409 CPAN-Meta-YAML-0.010 CPAN-Meta-Requirements-2.125 CPAN-Meta-2.133380 Module-Metadata-1.000019 version-0.9907 Sub-Uplevel-0.24 Test-Exception-0.32 Test-Simple-1.001002 Data-Dumper-2.145 Carp-1.32 File-Slurp-9999.19 ExtUtils-CBuilder-0.280212 ExtUtils-ParseXS-3.22 Perl-OSType-1.007 Test-Differences-0.61 Test-Harness-3.30 Test-Most-0.33 Exception-Class-1.37 Devel-StackTrace-1.31 Text-Diff-1.41 DBI-1.631 Devel-StackTrace-1.31 Exception-Class-1.37 GD-2.50 JSON-PP-2.27203 Data-Stag-0.14 URI-1.60 Module-Build-0.4204 DBD-SQLite-1.40 IPC-Run-0.92 Graph-0.96 GraphViz-2.15 XML-NamespaceSupport-1.11 XML-SAX-Base-1.08 XML-Parser-2.41 XML-SAX-0.99 XML-Simple-2.20 XML-Twig-3.44 XML-SAX-Writer-0.54 XML-Filter-BufferText-1.01 Acme-Damn-0.02 Bit-Vector-7.3 DBD-Pg-3.0.0 Clone-0.36 Class-Load-0.20 Task-Weaken-1.04 Sub-Exporter-Progressive-0.001011 Devel-GlobalDestruction-0.12 Sub-Name-0.05 Eval-Closure-0.11 Dist-CheckConflicts-0.10 Data-OptList-0.109 Moose-2.1202 Module-Runtime-0.013 Params-Util-1.07 Sub-Install-0.927 Module-Implementation-0.07 Try-Tiny-0.19 List-MoreUtils-0.33 Package-Stash-0.36 Package-DeprecationManager-0.13 MRO-Compat-0.12 Sub-Exporter-0.987 Compress-Raw-Zlib-2.065 Compress-Raw-Bzip2-2.064 Convert-Binary-C-0.76 Mozilla-CA-20130114 WWW-RobotRules-6.02 HTTP-Cookies-6.01 HTTP-Daemon-6.01 HTML-Tagset-3.20 HTML-Parser-3.71 HTTP-Negotiate-6.01 File-Listing-6.04 HTTP-Date-6.02 IO-HTML-1.00 HTTP-Message-6.06 Encode-Locale-1.03 LWP-MediaTypes-6.02 libwww-perl-6.05 Net-HTTP-6.06 Net-SSLeay-1.58 IO-Socket-SSL-1.966 LWP-Protocol-https-6.04 MIME-Base64-3.14 Crypt-SSLeay-0.64 Math-Random-0.71 Perl-Unsafe-Signals-0.02 Socket6-0.25 Storable-2.45 String-Approx-3.26 Tk-804.032 Sys-SigAction-0.21 XML-LibXML-2.0110 Data-Utilities-0.04 Time-HiRes-1.9726 Time-Piece-1.27 Want-0.22 DIYA-1.0 YAML-0.95 local-lib-2.000012 Statistics-Descriptive-3.0607

%define BUILDPL BioPerl-1.6.923 Class-Load-XS-0.06 

# Module-Build-0.4204 Tree-DAG_Node-1.20 Test-Warn-0.24 Test-Differences-0.61 Test-Harness-3.30 Test-Most-0.33 Exception-Class-1.37 Devel-StackTrace-1.31 Text-Diff-1.41

#
# FIXME
#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
There is a lot of stuff here including the following:
%{MODULES} %{BUILDPL}


#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

# %%setup

#------------------- %%build (~ configure && make) ----------------------------
%build

%include fasrcsw_module_loads.rpmmacros


export PERL5LIB=%{buildroot}/%{_prefix}/lib:%{buildroot}/%{_prefix}/lib/site_perl:$PERL5LIB
export PERL_MM_USE_DEFAULT=true

for m in %{MODULES}; do 
  cd %{_topdir}/BUILD
  tar xvf %{_topdir}/SOURCES/$m.tar.*

  cd %{_topdir}/BUILD/$m
  case $m in 
    XML-Twig*)
      perl Makefile.PL -y PREFIX=%{_prefix}
      ;;
    IO-Compress*)
      perl Makefile.PL INSTALL_BASE=%{_prefix}
      ;;
    *)
      perl Makefile.PL PREFIX=%{_prefix} 
      ;;
  esac
  make
  echo %{buildroot} | grep -q $m && rm -rf %{buildroot}
  mkdir -p %{buildroot}/%{_prefix}
  make install DESTDIR=%{buildroot}
done


for m in %{BUILDPL}; do
  cd %{_topdir}/BUILD
  tar xvf %{_topdir}/SOURCES/$m.tar.*

  cd %{_topdir}/BUILD/$m
  case $m in 
    BioPerl*)
      perl Build.PL --install_base %{_prefix} --accept
      ;;
    *) 
      perl Build.PL --install_base %{_prefix} 
      ;;
   esac
  ./Build
  ./Build install --destdir %{buildroot}
done


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

# %%makeinstall
export PERL5LIB=%{buildroot}/%{_prefix}/lib:%{buildroot}/%{_prefix}/lib/site_perl:$PERL5LIB

for m in %{MODULES}; do 
  cd %{_topdir}/BUILD/$m
  make install DESTDIR=%{buildroot}
done

for m in %{BUILDPL}; do
  cd %{_topdir}/BUILD/$m
  ./Build install --destdir %{buildroot}
done

test -e '%{buildroot}/%{_prefix}' || mkdir -p '%{buildroot}/%{_prefix}' 

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
        a = string.match(i,"^[^/]+")
        if not isloaded(a) then
            load(i)
        end
    end
end


---- environment changes (uncomment what is relevant)
prepend_path("PATH",                "%{_prefix}/bin")
prepend_path("PERL5LIB",              "%{_prefix}/lib")
prepend_path("PERL5LIB",              "%{_prefix}/lib/site_perl")
prepend_path("PERL5LIB",              "%{_prefix}/lib/perl5")
prepend_path("MANPATH",             "%{_prefix}/man")
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
