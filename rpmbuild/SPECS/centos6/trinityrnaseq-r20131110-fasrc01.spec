#------------------- package info ----------------------------------------------

#
# FIXME
#
# enter the simple app name, e.g. myapp
#
Name: trinityrnaseq

#
# FIXME
#
# enter the app version, e.g. 0.0.1
#
Version: r20131110

#
# FIXME
#
# enter the base release; start with fasrc01 and increment in subsequent 
# releases; the actual "Release" is constructed dynamically and set below
#
%define release_short fasrc01

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
%define summary_static Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data.
Summary: %{summary_static}

#
# FIXME
#
# enter the url from where you got the source, as a comment; change the archive 
# suffix if applicable
#
# http://downloads.sourceforge.net/project/trinityrnaseq/trinityrnaseq_r20131110.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Ftrinityrnaseq%2Ffiles%2F&ts=1392218381&use_mirror=superb-dca2

Source: %{name}_%{version}.tar.gz

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
# FIXME
#
# enter a description, often a paragraph; unless you prefix lines with spaces, 
# rpm will format it, so no need to worry about the wrapping
#
%description
Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes. 



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# FIXME
#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

# %%setup
cd %{_topdir}/BUILD
tar xvf %{_topdir}/SOURCES/%{name}_%{version}.tar.*


#------------------- %%build (~ configure && make) ----------------------------

%build

#
# FIXME
#
# configure and make the software here; the default below is for standard 
# GNU-toolchain style things
# 

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

##prerequisite apps (uncomment and tweak if necessary)
#module load NAME/VERSION-RELEASE
# This actually does the "install" target in the Makefile

cd %{_topdir}/BUILD/%{name}_%{version}
make



#------------------- %%install (~ make install + create modulefile) -----------

%install

#
# FIXME
#
# make install here; the default below is for standard GNU-toolchain style 
# things; plus we add some handy files (if applicable) and build a modulefile
#
# TIP -- first run rmpbuild with --define 'inspect yes' in order to stop after 
# the make install step and see what to include in the modulefile, the %%files 
# section, etc.
#

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

cd %{_topdir}/BUILD/%{name}_%{version}
echo %{buildroot} | grep -q %{name}_%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
cp -r * %{buildroot}/%{_prefix}

#these files are nice to have; %%doc is not as prefix-friendly as I would like
#if there are other files not installed by make install, add them here
for f in COPYING AUTHORS README INSTALL ChangeLog NEWS THANKS TODO BUGS; do
	test -e "$f" && ! test -e '%{buildroot}/%{_prefix}/'"$f" && cp -a "$f" '%{buildroot}/%{_prefix}/'
done

#this is the part that allows for inspecting the build output without fully creating the rpm
#there should be no need to change this
%if %{defined inspect}
	set +x
	
	echo
	echo
	echo "*************** fasrcsw -- STOPPING due to %%define inspect yes ****************"
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
# FIXME (but the above is enough for an "inspect" trial build)
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
--if mode()=="load" then
--	if not isloaded("NAME") then
--		load("NAME/VERSION-RELEASE")
--	end
--end

---- environment changes (uncomment what's relevant)
prepend_path("PATH",               "%{_prefix}/Inchworm/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/slclust/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/ffindex/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/jellyfish/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/coreutils/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/transdecoder/util/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/transdecoder/3rd_party/ffindex/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/transdecoder/3rd_party/parafly/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/collectl/bin")
prepend_path("PATH",               "%{_prefix}/trinity-plugins/parafly/bin")
prepend_path("PATH",               "%{_prefix}/Butterfly/src/bin")
prepend_path("CPATH",              "%{_prefix}/trinity-plugins/slclust/include")
prepend_path("CPATH",              "%{_prefix}/trinity-plugins/ffindex/include")
prepend_path("CPATH",              "%{_prefix}/trinity-plugins/jellyfish/unit_tests/gtest/include")
prepend_path("CPATH",              "%{_prefix}/trinity-plugins/transdecoder/util/include")
prepend_path("CPATH",              "%{_prefix}/trinity-plugins/transdecoder/3rd_party/ffindex/include")
prepend_path("FPATH",              "%{_prefix}/trinity-plugins/slclust/include")
prepend_path("FPATH",              "%{_prefix}/trinity-plugins/ffindex/include")
prepend_path("FPATH",              "%{_prefix}/trinity-plugins/jellyfish/unit_tests/gtest/include")
prepend_path("FPATH",              "%{_prefix}/trinity-plugins/transdecoder/util/include")
prepend_path("FPATH",              "%{_prefix}/trinity-plugins/transdecoder/3rd_party/ffindex/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/trinity-plugins/coreutils/coreutils-8.17/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/trinity-plugins/transdecoder/experimental/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/Butterfly/src/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/trinity-plugins/coreutils/coreutils-8.17/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/trinity-plugins/transdecoder/experimental/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/Butterfly/src/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/trinity-plugins/ffindex/lib64")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/trinity-plugins/transdecoder/util/lib64")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/trinity-plugins/transdecoder/3rd_party/ffindex/lib64")
prepend_path("LIBRARY_PATH",       "%{_prefix}/trinity-plugins/ffindex/lib64")
prepend_path("LIBRARY_PATH",       "%{_prefix}/trinity-plugins/transdecoder/util/lib64")
prepend_path("LIBRARY_PATH",       "%{_prefix}/trinity-plugins/transdecoder/3rd_party/ffindex/lib64")
prepend_path("MANPATH",            "%{_prefix}/trinity-plugins/coreutils/coreutils-8.17/man")
prepend_path("MANPATH",            "%{_prefix}/trinity-plugins/collectl/man")
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
