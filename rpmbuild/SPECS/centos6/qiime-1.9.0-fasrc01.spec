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
%define summary_static QIIME version 1.9.0
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
#URL: http://...FIXME...
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
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
QIIME: Quantitative Insights Into Microbial Ecology. This module was built by Plamen G. Krastev.


#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep


#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things -- hopefully it'll just work as-is.
#



#------------------- %%build (~ configure && make) ----------------------------

%build

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
# configure and make the software here.  The default below is for standard 
# GNU-toolchain style things -- hopefully it'll just work as-is.
# 



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
# does not support this:
#
# https://github.com/fasrc/fasrcsw/blob/master/doc/FAQ.md#how-do-i-handle-apps-that-insist-on-writing-directly-to-the-production-location
#
# %%{buildroot} is usually ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.%{arch}.
# (A spec file cannot change it, thus it is not inside $FASRCSW_DEV.)
#


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
--if mode()=="load" then
--	if not isloaded("NAME") then
--		load("NAME/VERSION-RELEASE")
--	end
--end

-- Dependencies --
load("pip/6.0.8-fasrc01")
load("jre/1.6.0_20-fasrc01")
load("ncbi-blast/2.2.22-fasrc01")
load("cd-hit/3.1.1-fasrc01")
load("chimeraslayer/2011.05.19-fasrc01")
load("muscle/3.8.31-fasrc01")
load("mothur/1.25.0-fasrc01")
load("clearcut/1.0.9-fasrc01")
load("raxml/7.3.0-fasrc01")
load("infernal/1.0.2-fasrc01")
load("muscle/3.8.31-fasrc01")
load("rtax/0.984-fasrc01")
load("usearch/5.2.236-fasrc01")
load("sumaclust/1.0.00-fasrc01")
load("swarm/1.2.19-fasrc01")
load("sortmerna/2.0-fasrc01")
load("ghc/7.8.3-fasrc01")
load("gsl/1.16-fasrc02")
load("AmpliconNoise/1.27-fasrc01")
load("cytoscape/2.7.0-fasrc01")
load("R/3.1.0-fasrc01")
load("fasttree/2.1.3-fasrc01") 
load("pplacer/1.0.0-fasrc01")
load("ParsInsert/1.04-fasrc01")
load("ea-utils/1.1.2.537-fasrc01")
load("SeqPrep/1.1-fasrc01")
load("hdf5/1.8.12-fasrc04")
load("gmp/6.0.0-fasrc02")

-- environment changes (uncomment what's relevant)
prepend_path("PATH",                              "/n/sw/centos6/qiime-1.9.0/bin")
prepend_path("PYTHONPATH",                        "/n/sw/centos6/qiime-1.9.0/lib/python2.7/site-packages")
setenv("QIIME_CONFIG_FP",                         "/n/sw/centos6/qiime-1.9.0/etc/qiime_config")
setenv("OMPI_MCA_btl_base_warn_component_unused", "0")
setenv("SOURCETRACKER_PATH",                      "/n/sw/centos6/sourcetracker-0.9.5")
setenv("RDP_JAR_PATH",                            "/n/sw/rdp_classifier_2.2/rdp_classifier-2.2.jar")
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
