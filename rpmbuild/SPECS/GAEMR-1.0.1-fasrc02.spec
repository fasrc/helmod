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
%define summary_static GAEMR v1.0.1
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://www.broadinstitute.org/software/gaemr/wp-content/uploads/2012/12/GAEMR-1.0.1.tar.gz
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


%define builddependencies %{nil}
%define rundependencies bib/2014.05.19-fasrc02 rdp_classifier/2.10.1-fasrc01 rnammer/1.2-fasrc01 python/2.7.6-fasrc01 picard-tools/1.119-fasrc01 
%define buildcomments %{nil}
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
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
The Genome Assembly Evaluation Metrics and Reporting (GAEMR) package is an assembly analysis framework composed a number of integrated modules. These modules can be executed as a single program to generate a complete analysis report, or executed individually to generate specific charts and tables. GAEMR standardizes input by converting a variety of read types to Binary Alignment Map (BAM) format, allowing a single input format to be entered into GAEMR’s analysis pipeline, hence enabling the generation of standard reports.

GAEMR’s analysis philosophy is centered on contiguity, correctness, and completeness -- how many pieces in an assembly composed of, how well those pieces accurately represent the genome sequenced, and how much of that genome is represented by those pieces. By performing over twenty different analyses based on these principles, GAEMR gives a clear picture of the condition of a genome assembly. For a broadly-defined list of these analyses, see the Features section in the documentation.

More information at http://www.broadinstitute.org/software/gaemr/

This installation has been configured to include paths for the required 3rd-party programs.

(Built and installed by Bob Freeman, PhD)


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
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}.tar.*
cd %{name}-%{version}
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

# ./configure --prefix=%{_prefix} \
# 	--program-prefix= \
# 	--exec-prefix=%{_prefix} \
# 	--bindir=%{_prefix}/bin \
# 	--sbindir=%{_prefix}/sbin \
# 	--sysconfdir=%{_prefix}/etc \
# 	--datadir=%{_prefix}/share \
# 	--includedir=%{_prefix}/include \
# 	--libdir=%{_prefix}/lib64 \
# 	--libexecdir=%{_prefix}/libexec \
# 	--localstatedir=%{_prefix}/var \
# 	--sharedstatedir=%{_prefix}/var/lib \
# 	--mandir=%{_prefix}/share/man \
# 	--infodir=%{_prefix}/share/info

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel

# make

# unfortunately, have to fix a config file to embed paths to tools needed for GAEMR. Ugh!
# MUMMER_PATH
sed -i 's@"/broad/software/groups/gtba/software/mummer_3.23-64bit/"@os.environ["BIB_PREFIX"] + "/active/bin/"@' gaemr/PlatformConstant.py
# BLAST_DIR
sed -i 's@"/broad/software/groups/gtba/software/ncbi-blast-2.2.25+/bin/"@os.environ["BIB_PREFIX"] + "/active/bin/"@' gaemr/PlatformConstant.py
# SAMTOOLS
sed -i 's@"/broad/software/groups/gtba/software/samtools_0.1.18/bin/samtools"@os.environ["BIB_PREFIX"] + "/active/bin/samtools"@' gaemr/PlatformConstant.py
# PICARD
sed -i 's@"/seq/software/picard/current/bin/"@os.environ["PICARD_TOOLS_HOME"]@' gaemr/PlatformConstant.py
# BLAST_NT
sed -i 's@"/broad/data/blastdb/nt/nt"@os.environ["HUIFX_DB_CUSTOM"] + "/blastdb/nt"@' gaemr/PlatformConstant.py
# BLAST_UNIVEC
sed -i 's@"/gsap/assembly_analysis/databases/UniVec/UniVec"@os.environ["HUIFX_DB_CUSTOM"] + "/blastdb/UniVec"@' gaemr/PlatformConstant.py
# BLAST_rRNA
sed -i 's@"/gsap/assembly_analysis/databases/NCBI_rRNA/ncbi_rRNA"@os.environ["HUIFX_DB_CUSTOM"] + "/blastdb/ncbi_rRNA"@' gaemr/PlatformConstant.py
# BLAST_MITOGCONTAM
sed -i 's@"/gsap/assembly_analysis/databases/mitogcontam/mitogcontam"@os.environ["HUIFX_DB_CUSTOM"] + "/other/mitogcontam"@' gaemr/PlatformConstant.py
# TAX NODES/names
sed -i 's@"/broad/data/taxonomy/taxdump/nodes.dmp"@os.environ["HUIFX_DB_CUSTOM"] + "/taxonomy/nodes.dmp"@' gaemr/PlatformConstant.py
sed -i 's@"/broad/data/taxonomy/taxdump/names.dmp"@os.environ["HUIFX_DB_CUSTOM"] + "/taxonomy/names.dmp"@' gaemr/PlatformConstant.py
# RNAMMER
sed -i 's@"/seq/annotation/bio_tools/rnammer/current/rnammer"@os.environ["RNAMMER_HOME"]@' gaemr/PlatformConstant.py
# RDP_CLASSIFIER
sed -i 's@"/broad/software/groups/gtba/software/rdp_classifier_2.4/rdp_classifier-2.4.jar"@os.environ["RDP_CLASSIFIER_HOME"] + "/classifier.jar"@' gaemr/PlatformConstant.py
# BWA
sed -i 's@"/seq/software/picard/current/3rd_party/bwa"@os.environ["BIB_PREFIX"] + "/active/bin/"@' gaemr/PlatformConstant.py
# GAEMR
sed -i 's@"/gsap/assembly_analysis/GAEMR/bin/"@os.environ["GAEMR_HOME"] + "/bin/"@' gaemr/PlatformConstant.py
# BOWTIE
sed -i 's@"/broad/software/free/Linux/redhat_5_x86_64/pkgs/bowtie2_2.0.0-beta5/"@os.environ["BIB_PREFIX"] + "/active/bin/"@' gaemr/PlatformConstant.py

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

# make install DESTDIR=%{buildroot}
cp -R * %{buildroot}/%{_prefix}

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



-- environment changes (uncomment what is relevant)
setenv("GAEMR_HOME",                "%{_prefix}")
setenv("HUIFX_DB_CUSTOM",           "/n/regal/informatics_public/custom")
prepend_path("PATH",                "%{_prefix}/bin")
prepend_path("PYTHONPATH",          "%{_prefix}")
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
