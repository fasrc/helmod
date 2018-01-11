#
# See also: misc/make_bib_wrapper_modules
#

# The spec involves the hack that allows the app to write directly to the 
# production location.  The following allows the production location path to be 
# used in files that the rpm builds.
%define __arch_install_post %{nil}


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
%define summary_static the cross-platform package manager for command-line bioinformatics tools
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: http://bib.bitbucket.org/
#Source: %{name}-%{version}.tar.gz
#wget https://bitbucket.org/mhowison/bib/raw/master/install.sh -O bib-2015.02.27-install.sh
#chmod a+x bib-2015.02.27-install.sh

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
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
BiB is a cross-platform manager for command-line bioinformatics tools. This
For more information and examples of how to use BiB, see http://bib.bitbucket.org.



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep


#
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things -- hopefully it'll just work as-is.
#

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD 
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
cp "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}-install.sh .
chmod -Rf a+rX,u+w,g-w,o-w .



#------------------- %%build (~ configure && make) ----------------------------

%build

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
#
# configure and make the software here.  The default below is for standard 
# GNU-toolchain style things -- hopefully it'll just work as-is.
# 

##prerequisite apps (uncomment and tweak if necessary).  If you add any here, 
##make sure to add them to modulefile.lua below, too!
#module load NAME/VERSION-RELEASE

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel



#------------------- %%install (~ make install + create modulefile) -----------

%install

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
# make install here.  The default below is for standard GNU-toolchain style 
# things -- hopefully it'll just work as-is.
#
# Note that DESTDIR != %{prefix} -- this is not the final installation.  
# Rpmbuild does a temporary installation in the %{buildroot} and then 
# constructs an rpm out of those files.  See the following hack if your app 
# does not support this:/etc/profile.d/modules.sh
#
# https://github.com/fasrc/fasrcsw/blob/master/doc/FAQ.md#how-do-i-handle-apps-that-insist-on-writing-directly-to-the-production-location
#
# %%{buildroot} is usually ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{arch}.
# (A spec file cannot change it, thus it is not inside $FASRCSW_DEV.)
#


#
# This app insists on writing directly to the prefix.  Acquiesce, and hack a 
# symlink, IN THE PRODUCTION DESTINATION (yuck), back to our where we want it
# to install in our build environment, and then remove the symlink.  Note that 
# this will only work for the first build of this NAME/VERSION/RELEASE/TYPE 
# combination.
#

# Standard stuff.
umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

# Make the symlink.
sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true
sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"


#base installation
bash ./%{name}-%{version}-install.sh "%{_prefix}"

#install everything possible; see:
#https://bitbucket.org/mhowison/bib/src/6628788b026160af254725b43fae9e48c6647e39/recipes/?at=master
export BIB_PREFIX="%{_prefix}"
export PATH="%{_prefix}/active/bin:$PATH"
yes | bib install abyss
yes | bib install bamtools
yes | bib install biolite-tools
yes | bib install blast
yes | bib install bowtie
yes | bib install bowtie2
yes | bib install bwa
yes | bib install fasta
yes | bib install fastqc
yes | bib install fermi
yes | bib install gblocks
yes | bib install google-sparsehash
yes | bib install gsl
yes | bib install hmmer
yes | bib install jellyfish
yes | bib install macse
yes | bib install mafft
yes | bib install mcl
yes | bib install mummer
yes | bib install oases
yes | bib install parallel
yes | bib install raxml
yes | bib install rsem
yes | bib install samtools
yes | bib install spimap
yes | bib install sratoolkit
yes | bib install swipe
yes | bib install transdecoder
yes | bib install trinity
yes | bib install velvet
#note:  you'll still see a lot of the following lines:
#   Ready to install.  Press ENTER to continue with the install.
#followed by a pause, but it's actually doing stuff

#this was NOT done for bib-2014.05.19-fasrc01; staging for next time
#to fix this:
#	$ pwd
#	/n/sw/fasrcsw/apps/Core/bib/2014.05.19-fasrc01
#	$ find . >/dev/null
#	find: `./install/samtools/0.1.19': Permission denied
#	find: `./install/gblocks/0.91b': Permission denied
#	find: `./install/bowtie/1.0.0': Permission denied
#	$ ls -alFd ./install/samtools/0.1.19 ./install/gblocks/0.91b ./install/bowtie/1.0.0
#	drwxrwx--- 8 root root 3149 2014-05-19 14:06:30 ./install/bowtie/1.0.0/
#	drwx------ 4 root root  138 2014-05-19 14:06:41 ./install/gblocks/0.91b/
#	drwxr-x--- 7 root root 2822 2014-05-19 14:07:31 ./install/samtools/0.1.19/

chmod -R go+rX "%{_prefix}"/install
chmod -R go-w  "%{_prefix}"/install

# For some reason, you have to run jellyfish 
%{_prefix}/install/trinity/2.0.6/trinity-plugins/jellyfish/bin/jellyfish --help

# Clean up the symlink.  (The parent dir may be left over, oh well.)
sudo rm "%{_prefix}"


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
setenv("BIB_PREFIX", "%{_prefix}")
prepend_path("PATH", "%{_prefix}/active/bin")

-- added 10/21/14, rmf to include relevant library paths
prepend_path("CPATH", "%{_prefix}/active/include")
prepend_path("FPATH", "%{_prefix}/active/include")
prepend_path("LD_LIBRARY_PATH", "%{_prefix}/active/lib")
prepend_path("LIBRARY_PATH", "%{_prefix}/active/lib")
prepend_path("MANPATH", "%{_prefix}/active/man")
-- end add

-- (there are lots of other standard looking dirs, but the directions say only 
-- a PATH update is needed)
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
%{_prefix}/.git
%{_prefix}/.gitignore



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
