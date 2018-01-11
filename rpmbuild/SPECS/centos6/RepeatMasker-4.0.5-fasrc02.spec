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
%define summary_static RepeatMasker (open) v4.0.5
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://www.repeatmasker.org/RepeatMasker-open-4-0-5.tar.gz
Source: %{name}-open-4-0-5.tar.gz

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


%define builddependencies perl-modules/5.10.1-fasrc11 trf/404-fasrc01 ncbi-rmblastn/2.2.28-fasrc01 hmmer/3.1b1-fasrc01
%define rundependencies %{builddependencies}
%define buildcomments Updated to dependency on newer perl modules
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
%description
RepeatMasker is a program that screens DNA sequences for interspersed repeats and low complexity DNA sequences. The output of the program is a detailed annotation of the repeats that are present in the query sequence as well as a modified version of the query sequence in which all the annotated repeats have been masked (default: replaced by Ns). Sequence comparisons in RepeatMasker are performed by one of several popular search engines including nhmmer, cross_match, ABBlast/WUBlast, RMBlast and Decypher. RepeatMasker makes use of curated libraries of repeats and currently supports Dfam ( profile HMM library derived from Repbase sequences ) and Repbase, a service of the Genetic Information Research Institute.


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
rm -rf %{name}-%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-open-4-0-5.tar.gz
mv %{name} %{name}-%{version}
cd %{name}-%{version}

# get current RepeatMasker library
wget --no-clobber http://BobFreemanMA:g70lb2@www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/repeatmaskerlibraries-20140131.tar.gz
tar zxfv repeatmaskerlibraries-20140131.tar.gz 
rm repeatmaskerlibraries-20140131.tar.gz 

# get current Dfam library
wget --no-clobber ftp://selab.janelia.org/pub/dfam/Current_Release/Dfam.hmm.gz
gunzip Dfam.hmm.gz 
mv Dfam.hmm Libraries/

# and back to our regularly scheduled work...
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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}


cat > RepeatMaskerConfig.pm <<EOF
#!/usr/bin/env perl
##---------------------------------------------------------------------------##
##  File:
##      @(#) RepeatMaskerConfig.pm
##  Author:
##      Arian Smit <asmit@systemsbiology.org>
##      Robert Hubley <rhubley@systemsbiology.org>
##  Description:
##      This is the main configuration file for the RepeatMasker
##      program suite.  Before you can run the programs included
##      in this package you will need to edit this file and
##      configure for your site.  NOTE: There is also a "configure"
##      script which will help you do this.
##
#******************************************************************************
#* Copyright (C) Institute for Systems Biology 2005 Developed by
#* Arian Smit and Robert Hubley.
#*
#* This work is licensed under the Open Source License v2.1.  To view a copy
#* of this license, visit http://www.opensource.org/licenses/osl-2.1.php or
#* see the license.txt file contained in this distribution.
#*
###############################################################################
package RepeatMaskerConfig;
use FindBin;
require Exporter;
@EXPORT_OK = qw( \$REPEATMASKER_DIR \$REPEATMASKER_MATRICES_DIR
    \$REPEATMASKER_LIB_DIR \$WUBLAST_DIR \$WUBLASTN_PRGM
    \$WUBLASTP_PRGM \$WUBLASTX_PRGM \$SETDB_PRGM \$XDFORMAT_PRGM 
    \$DEMAKE \$DECYPHER \$LIBPATH \$TRF_PRGM \$DEBUGALL \$VALID_SEARCH_ENGINES
    \$DEFAULT_SEARCH_ENGINES \$RMBLAST_DIR \$RMBLASTN_PRGM \$RMBLASTDB_PRGM );

%%EXPORT_TAGS = ( all => [ @EXPORT_OK ] );
@ISA         = qw(Exporter);

BEGIN {
##----------------------------------------------------------------------##
##     CONFIGURE THE FOLLOWING PARAMETERS FOR YOUR INSTALLATION         ##
##                                                                      ##
##
## RepeatMasker Location
## ======================
## The path to the RepeatMasker programs and support files
## This is the directory with this file as well as
## the ProcessRepeats and Library/ and Matrices/ subdirectories
## reside.
##
##    i.e. Typical UNIX installation
##     \$REPEATMASKER_DIR = "/usr/local/RepeatMasker";
##    Windows w/Cygwin example:
##     \$REPEATMASKER_DIR = "/cygdrive/c/RepeatMasker";
##
  \$REPEATMASKER_DIR          = "\$FindBin::RealBin";
  \$REPEATMASKER_MATRICES_DIR = "\$REPEATMASKER_DIR/Matrices";
  \$REPEATMASKER_LIB_DIR      = "\$REPEATMASKER_DIR/Libraries";

##
## Search Engine Configuration:
##   RepeatMasker uses either the CrossMatch, WUBlast/ABBlast, or the
##   TimeLogic search engine to find matches to interspersed
##   repeat consensi.  You are only required to have one engine
##   installed on your system in order to run RepeatMasker.  
##   
##   The optional program RepeatProteinMask will only run
##   with the WUBlast/ABBlast package ( currently ).  
##

  ##
  ## CrossMatch Location
  ## ===================
  ## The path to Phil Green's cross_match program ( phrap program suite ).
  ##   - Use cross_match version 980501 or later for best results
  ##   - On a windows machine running the cygwin emulation software
  ##     you might set this to something like this:
  ##
  ##            \$CROSSMATCH_DIR = "/cygdrive/c/phrap";
  ##            \$CROSSMATCH_PRGM = "cross_match.exe";
  ##
    \$CROSSMATCH_DIR = "/usr/local/bin";
    \$CROSSMATCH_PRGM = "\$CROSSMATCH_DIR/cross_match";

  ##
  ## HMMER Location
  ## ========================
  ## Set the location of the HMMER programs and support utilities.
  ##
    \$HMMER_DIR   = "/usr/local/hmmer";
    \$NHMMSCAN_PRGM = "\$HMMER_DIR/nhmmscan";
    \$HMMPRESS_PRGM = "\$HMMER_DIR/hmmpress";

  ##
  ## RMBlast Location
  ## ========================
  ## Set the location of the NCBI RMBLAST programs and support utilities.
  ##
    \$RMBLAST_DIR   = "${RMBLAST_HOME}/bin";
    \$RMBLASTN_PRGM = "\$RMBLAST_DIR/rmblastn";
    \$RMBLASTX_PRGM = "\$RMBLAST_DIR/blastx";
    \$RMBLASTDB_PRGM   = "\$RMBLAST_DIR/makeblastdb";
 
  ##
  ## WUBLAST/ABBlast Location
  ## ========================
  ## Set the location of the WUBLAST/ABBlast programs and support utilities.
  ##
    \$WUBLAST_DIR   = "/usr/local/abblast";
    \$WUBLASTN_PRGM = "\$WUBLAST_DIR/blastn";
    \$WUBLASTP_PRGM = "\$WUBLAST_DIR/blastp";
    \$WUBLASTX_PRGM = "\$WUBLAST_DIR/blastx";
    \$XDFORMAT_PRGM = "\$WUBLAST_DIR/xdformat";
    \$SETDB_PRGM    = "\$WUBLAST_DIR/setdb";
  
  ##
  ## DeCypher Blast ( OPTIONAL )
  ## ==============
  ##  Location of TimeLogic's DeCypher Blast
  ##  ie. 
  ##    \$DECYPHER = "c:/dc_local/bin/dc_template_rt";
  ##
  ##
    \$DEMAKE  = "dc_make_target -template format_aa_into_aa -quiet";
    \$DECYPHER = "";
  
  
##
## Default Search Engine
## =====================
##  Pick which search engine should be the default
##  Can be one of "crossmatch", "wublast", "decypher" or "ncbi".
##
  \$DEFAULT_SEARCH_ENGINE = "ncbi";


##
## Library Path
## ============
##   - RepeatMasker now generates and caches
##     species specific libraries.  The LIBPATH 
##     parameter defines the search order for
##     directories where library caches might
##     be stored.  NOTE: RepeatMasker needs at
##     least one of these directories to be writable
##     and thus if it can't read a cached library
##     from one of these locations, or write
##     a new library in one of these locations it
##     will default to building the libraries
##     in the programs work directory every time
##     it runs -- this could be slow if you commonly
##     run against short sequences using the same
##     species parameters.
##
  @LIBPATH = ( \$REPEATMASKER_LIB_DIR, 
               \$ENV{'HOME'} . "/.RepeatMaskerCache" );


##
## TRF Location ( OPTIONAL )
## ============
## Tandem Repeat Finder program.  This is only required by
## the RepeatProteinMask program.
##
  \$TRF_PRGM = "${TRF_HOME}/trf";

##
## Turns on debugging in all RepeatMasker modules/scripts
##
  \$DEBUGALL = 0;

##                                                                      ##
##                      END CONFIGURATION AREA                          ##
##----------------------------------------------------------------------##

##----------------------------------------------------------------------##
## Do not change these parameters
##
  \$VALID_SEARCH_ENGINES = { "crossmatch" => 1, 
                            "wublast" => 1, 
                            "decypher" => 1  };

##----------------------------------------------------------------------##
}

1;
EOF


# fix hard coding of perl location...
find . -type f -mtime -1 | xargs sed -i "s@${PERL_HOME}/bin/perl@/usr/bin/env perl@"

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel

# No need for RepeatMasker
#make



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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
#make install DESTDIR=%{buildroot}
cp -r * %{buildroot}%{_prefix}

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
setenv("REPEATMASKER_HOME",         "%{_prefix}")
prepend_path("PATH",                "%{_prefix}")
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
