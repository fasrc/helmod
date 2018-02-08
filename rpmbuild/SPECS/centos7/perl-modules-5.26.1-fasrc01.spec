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
#Source: %{name}-%{version}.tar.gz

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
# The list of modules installed 
#
# NOTE: If you need to version of the modules in a future install, the latest versions of the same modules can be downloaded automatically 
# from cpan, for example, feeding the following list to something like 
# [francesco@builds02 New-Perl-Mods]$ mylist="ExtUtils-MakeMaker-6.98 IO-String-1.08 Test-Deep-0.112"
# [francesco@builds02 New-Perl-Mods]$ for i in `echo $mylist | sed 's/-[0-9]\+\(\.[0-9]\+\)*//g' | sed 's/-/::/g'` ; do cpan -g $i ; done 
# [francesco@builds02 New-Perl-Mods]$ ls *gz  
# ExtUtils-MakeMaker-7.30.tar.gz  IO-String-1.08.tar.gz  Test-Deep-1.127.tar.gz
# [francesco@builds02 New-Perl-Mods]$  ls *gz | sed 's/.tar.gz//g' | tr '\n' ' '
# ExtUtils-MakeMaker-7.30 IO-String-1.08 Test-Deep-1.127
# 
# This is true for everything in the list except for :
# Scalar-List-Utils : search for  Scalar::Util
# TermReadKey       : search for  Term::ReadKey
# TimeDate          : search for  Date::Format
# libwww-perl       : search for  LWP 
# DIYA  ..... https://github.com/bioteam/DIYA most likely abandoned project (last commit was march 2013. but someone may still need it.
# 
# Also, in the build the modules are supposed to be in tar.gz archives. please check that there are no bz2 or other extensions.
#
%define MODULES Text-Diff-1.45 Text-Glob-0.11 Capture-Tiny-0.46 Try-Tiny-0.30 Test-Deep-1.127 Test-Differences-0.64 Test-Exception-0.43 Test-Harness-3.39 Test-Most-0.35 Test-Simple-1.302120 Test-Warn-0.32 Test-Fatal-0.014 Test-Needs-0.002005  Module-Build-0.4224 Module-Implementation-0.09 Module-Metadata-1.000033 Module-Runtime-0.016  Package-DeprecationManager-0.17 Package-Stash-0.37 Test-Needs-0.002005 Acme-Damn-0.08 Algorithm-Diff-1.1903 Carp-1.38 Bit-Vector-7.4 Class-Data-Inheritable-0.08 Path-Class-0.37 Data-Dumper-2.161 Data-OptList-0.110 Data-Utilities-0.04 Class-Load-0.24 Clone-0.39 XML-Filter-BufferText-1.01 XML-LibXML-2.0132 XML-NamespaceSupport-1.12 XML-Parser-2.44 XML-SAX-0.99 XML-SAX-Base-1.09 XML-SAX-Writer-0.57 XML-Simple-2.24 XML-Twig-3.52 YAML-1.24 Compress-Raw-Bzip2-2.074 Compress-Raw-Zlib-2.076 Convert-Binary-C-0.78 CPAN-Meta-2.150010 CPAN-Meta-Requirements-2.140 CPAN-Meta-YAML-0.018 Crypt-SSLeay-0.72 DBD-Pg-3.7.0 DBD-SQLite-1.54 DBI-1.640 Devel-GlobalDestruction-0.14 Devel-StackTrace-2.03 Dist-CheckConflicts-0.11 Email-Date-Format-1.005 Encode-Locale-1.05 Eval-Closure-0.14 Exception-Class-1.44 ExtUtils-CBuilder-0.280230 ExtUtils-F77-1.20 ExtUtils-MakeMaker-7.30 ExtUtils-ParseXS-3.35 File-Copy-Link-0.140 File-Listing-6.04 File-ShareDir-Install-0.11 File-Slurp-9999.19 File-Which-1.22 forks-0.36 GD-2.67 Graph-0.9704 GraphViz-2.24 Hash-Merge-0.299 HTML-Parser-3.72 HTML-Tagset-3.20 HTTP-Cookies-6.04 HTTP-Daemon-6.01 HTTP-Date-6.02 HTTP-Message-6.14 HTTP-Negotiate-6.01 Inline-0.80 Inline-C-0.78 IO-All-0.87 IO-HTML-1.001 IO-Prompt-0.997004 IO-Socket-SSL-2.054 IO-String-1.08 IPC-Run-0.96 JSON-PP-2.97001 libwww-perl-6.31 List-MoreUtils-0.428 local-lib-2.000024 Logger-Simple-2.0 LWP-MediaTypes-6.02 LWP-Protocol-https-6.07 MailTools-2.20 Math-Matrix-0.8 Math-MatrixReal-2.13 Math-Random-0.72 MIME-Base64-3.15 MIME-Lite-3.030 MIME-Types-2.17 Moose-2.2009 Mozilla-CA-20160104 MRO-Compat-0.13 Net-HTTP-6.17 Net-SSLeay-1.84Parallel-ForkManager-1.19 Params-Util-1.07 Parse-RecDescent-1.967015 Perl-OSType-1.010 Perl-Unsafe-Signals-0.03 Scalar-List-Utils-1.49 Socket6-0.28 Spreadsheet-WriteExcel-2.40 Statistics-Descriptive-3.0612 Storable-2.51 String-Approx-3.28 Sub-Exporter-0.987 Sub-Exporter-Progressive-0.001013 Sub-Install-0.928 Sub-Name-0.21 Sub-Uplevel-0.2800 SVG-2.82 Sys-SigAction-0.23 Task-Weaken-1.05 TermReadKey-2.37 Time-HiRes-1.9753 Time-Piece-1.3203 Tk-804.034 Tree-DAG_Node-1.30  URI-1.73 version-0.9918 Want-0.29 Data-Stag-0.14  WWW-RobotRules-6.02  DIYA-1.0

%define BUILDPL BioPerl-1.007002 Class-Load-XS-0.10 Astro-FITS-Header-3.07

%define PDL PDL-2.018 

#
# FIXME
#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
Built against the fasrc01 release of perl-5.26.1.  There is a lot of stuff here including the following:
%{MODULES} %{BUILDPL} 

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



%define builddependencies  perl/5.26.1-fasrc01 
%define rundependencies %{builddependencies}
%define buildcomments Set HTTP_CA_FILE, "Module list: %{MODULES}"
%define requestor %{nil}
%define requestref %{nil}

# apptags
# For aci-ref database use aci-ref-app-category and aci-ref-app-tag namespaces and separate tags with a semi-colon
# aci-ref-app-category:Programming Tools; aci-ref-app-tag:Compiler
%define apptags aci-ref-app-category:Libraries; aci-ref-app-tag:Perl
%define apppublication %{nil}


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
#export PERL_MM_USE_DEFAULT=true

mkdir -p %{buildroot}/%{_prefix}
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
#  echo %{buildroot} | grep -q $m && rm -rf %{buildroot}
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

#
# Doing PDL as a special case because it is dependent on a Build.PL
# module (Astro::FITS::Header) and there are problems with the build
#
cd %{_topdir}/BUILD
tar xvf %{_topdir}/SOURCES/%{PDL}.tar.*
cd %{_topdir}/BUILD/%{PDL}

sed -i -e 's?sub MY::postamble {.*?sub MY::postamble {\
   return "";? ' Makefile.PL
perl Makefile.PL PREFIX=%{_prefix}

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
        if not isloaded(i) then
            load(i)
        end
    end
end

---- environment changes (uncomment what is relevant)
setenv("PERLMODULES_HOME",          "%{_prefix}")
setenv("HTTPS_CA_FILE",             "/etc/ssl/certs/ca-bundle.crt")
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
module              : %{modulename}
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
