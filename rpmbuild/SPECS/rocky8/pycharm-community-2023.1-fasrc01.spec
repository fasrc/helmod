#------------------- package info ----------------------------------------------

# binary package
%define __prelink_undo_cmd %{nil}

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
%define summary_static a Python IDE with smart code completion, code inspections, on-the-fly error highlighting and quick-fixes, along with automated code refactorings and rich navigation capabilities
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://download.jetbrains.com/python/pycharm-community-2020.1.1.tar.gz
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
PyCharm provides smart code completion, code inspections, on-the-fly error highlighting and quick-fixes, along with automated code refactorings and rich navigation capabilities (https://www.jetbrains.com/pycharm)



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep

#
# unpack the sources here.  The default below is for standard, GNU-toolchain 
# style things
#

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD
rm -rf %{name}_%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-%{version}.tar.gz
cd %{name}-%{version}
chmod -Rf a+rX,u+w,g-w,o-w .



#------------------- %%build (~ configure && make) ----------------------------

%build

#
# configure and make the software here; the default below is for standard 
# GNU-toolchain style things
# 

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

##prerequisite apps (uncomment and tweak if necessary)
#module load NAME/VERSION-RELEASE

#(do nothing)



#------------------- %%install (~ make install + create modulefile) -----------

%install

#
# make install here; the default below is for standard GNU-toolchain style 
# things; plus we add some handy files (if applicable) and build a modulefile
#

#(leave this here)
%include fasrcsw_module_loads.rpmmacros

#--- This app insists on writing directly to the prefix.  Complicating, things, 
#    it also insists that the prefix not exist, so even the symlink hack needs 
#    to be further hacked (introduce an additional sub-directory).


umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
cp -r * %{buildroot}/%{_prefix}


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

-- environment changes (uncomment what is relevant)
prepend_path("PATH",               "%{_prefix}/jbr/bin")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/jbr/include")
prepend_path("CPATH",              "%{_prefix}/plugins/python-ce/helpers/py3only/docutils/parsers/rst/include")
prepend_path("CPATH",              "%{_prefix}/plugins/python-ce/helpers/py2only/docutils/parsers/rst/include")
prepend_path("FPATH",              "%{_prefix}/jbr/include")
prepend_path("FPATH",              "%{_prefix}/plugins/python-ce/helpers/py3only/docutils/parsers/rst/include")
prepend_path("FPATH",              "%{_prefix}/plugins/python-ce/helpers/py2only/docutils/parsers/rst/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/jbr/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/pycharm-community-customization/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/color-scheme-twilight/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/qodana/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/grazie/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/color-scheme-github/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/searchEverywhereMl/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/marketplace/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/dev/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/cwm-plugin-projector/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/toml/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/pycharm-community-sharedIndexes-bundled/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/packageChecker/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/vcs-github/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/reStructuredText/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/editorconfig/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/color-scheme-warmNeon/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/vcs-git/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/properties/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/yaml/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/tasks/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/configurationScript/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/color-scheme-monokai/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/cwm-plugin/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/space/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/indexing-shared/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/emojipicker/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/featuresTrainer/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/vcs-hg/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/platform-images/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/completionMlRanking/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/settingsSync/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/sh/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/vcs-svn/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/python-sharedIndexes-downloadable/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/python-ce/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/python-ce/helpers/typeshed/stubs/caldav/caldav/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/markdown/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/copyright/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/terminal/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/platform-langInjection/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/plugins/textmate/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/jbr/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/pycharm-community-customization/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/color-scheme-twilight/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/qodana/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/grazie/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/color-scheme-github/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/searchEverywhereMl/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/marketplace/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/dev/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/cwm-plugin-projector/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/toml/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/pycharm-community-sharedIndexes-bundled/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/packageChecker/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/vcs-github/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/reStructuredText/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/editorconfig/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/color-scheme-warmNeon/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/vcs-git/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/properties/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/yaml/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/tasks/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/configurationScript/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/color-scheme-monokai/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/cwm-plugin/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/space/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/indexing-shared/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/emojipicker/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/featuresTrainer/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/vcs-hg/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/platform-images/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/completionMlRanking/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/settingsSync/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/sh/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/vcs-svn/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/python-sharedIndexes-downloadable/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/python-ce/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/python-ce/helpers/typeshed/stubs/caldav/caldav/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/markdown/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/copyright/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/terminal/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/platform-langInjection/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/plugins/textmate/lib")
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
