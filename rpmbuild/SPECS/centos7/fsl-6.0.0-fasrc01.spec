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
# enter a succinct one-line summary (%%{summary} gets changed when the debuginfo 
# rpm gets created, so this stores it separately for later re-use); do not 
# surround this string with quotes
#
%define summary_static FMRIB Software Library
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-6.0.0.tar.gz
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


%define builddependencies libpng/1.6.25-fasrc01
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
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
FSL is a comprehensive library of analysis tools for FMRI, MRI and DTI brain imaging data.

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

#python fslinstaller.py -d "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/fsl -q -D -V 6.0.0

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel




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
cp -r "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/* %{buildroot}/%{_prefix}

#make install DESTDIR=%{buildroot}


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


---- environment changes (uncomment what is relevant)
setenv("FSL_HOME",                  "%{_prefix}")
setenv("FSLDIR",                    "%{_prefix}")
setenv("FSLOUTPUTTYPE",             "NIFTI_GZ")
setenv("FSLMULTIFILEQUIT",          "TRUE")
setenv("FSLTCLSH",                  "%{_prefix}/bin/fsltclsh"))
setenv("FSLCONFDIR",                "%{_prefix}/config"))
setenv("FSLWISH",                   "%{_prefix}/bin/fslwish"))
setenv("FSLMACHINELIST",            "")
setenv("FSLREMOTECALL",             "")
setenv("FSLLOCKDIR",                "")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("PATH",               "%{_prefix}/data/atlases/bin")
prepend_path("PATH",               "%{_prefix}/extras/bin")
prepend_path("PATH",               "%{_prefix}/extras/include/boost/libs/config/checks/architecture/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/chardet-3.0.4-py37_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/setuptools-40.2.0-py37_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/wheel-0.31.1-py37_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pip-10.0.1-py37_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/conda-4.5.11-py37_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/nibabel-2.2.1-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/bokeh-1.0.2-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/wheel-0.32.3-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/future-0.17.1-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pycodestyle-2.3.1-py36hf609f19_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pyflakes-1.6.0-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/distributed-1.25.0-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pylint-1.8.2-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/llvm-3.3-0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pygments-2.2.0-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/setuptools-40.6.2-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pyqt-5.6.0-py36h22d08a2_6/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/isort-4.3.4-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/scikit-image-0.13.1-py36h14c3975_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/flake8-3.5.0-py36_1/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/pkgs/pip-18.1-py36_0/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/bin")
prepend_path("PATH",               "%{_prefix}/fslpython/envs/fslpython/bin")
prepend_path("PATH",               "%{_prefix}/src/mist-clean/bin")
prepend_path("CPATH",              "%{_prefix}/bin/FSLeyes/include")
prepend_path("CPATH",              "%{_prefix}/bin/FSLeyes/docutils/parsers/rst/include")
prepend_path("CPATH",              "%{_prefix}/extras/lib/libxml++-2.6/include")
prepend_path("CPATH",              "%{_prefix}/extras/src/libxml2-2.9.2/include")
prepend_path("CPATH",              "%{_prefix}/extras/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/boost/spirit/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/boost/spirit/repository/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/boost/fusion/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/libs/mpl/preprocessed/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/libs/phoenix/test/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/libs/numeric/ublas/IDEs/qtcreator/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/libs/chrono/stopwatches/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/build/test/railsys/program/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/build/test/railsys/libx/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/build/example/pch/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/build/example/libraries/util/foo/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/build/src/engine/boehm_gc/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/auto_index/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/boost/tools/quickbook/test/include")
prepend_path("CPATH",              "%{_prefix}/extras/include/armawrap/armawrap/armadillo-5.200.1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib/wx/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/lib/glib-2.0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/core/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/lib/dbus-1.0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtknetcdf/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtkoggtheora/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtkglew/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/llvm-3.3-0/lib/clang/3.3/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/llvm-3.3-0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/clang/3.3/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/glib-2.0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/dbus-1.0/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/wx/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/core/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtkglew/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtknetcdf/include")
prepend_path("CPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtkoggtheora/include")
prepend_path("CPATH",              "%{_prefix}/include")
prepend_path("FPATH",              "%{_prefix}/bin/FSLeyes/include")
prepend_path("FPATH",              "%{_prefix}/bin/FSLeyes/docutils/parsers/rst/include")
prepend_path("FPATH",              "%{_prefix}/extras/lib/libxml++-2.6/include")
prepend_path("FPATH",              "%{_prefix}/extras/src/libxml2-2.9.2/include")
prepend_path("FPATH",              "%{_prefix}/extras/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/boost/spirit/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/boost/spirit/repository/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/boost/fusion/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/libs/mpl/preprocessed/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/libs/phoenix/test/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/libs/numeric/ublas/IDEs/qtcreator/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/libs/chrono/stopwatches/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/build/test/railsys/program/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/build/test/railsys/libx/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/build/example/pch/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/build/example/libraries/util/foo/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/build/src/engine/boehm_gc/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/auto_index/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/boost/tools/quickbook/test/include")
prepend_path("FPATH",              "%{_prefix}/extras/include/armawrap/armawrap/armadillo-5.200.1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib/wx/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/lib/glib-2.0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/core/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/lib/dbus-1.0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtknetcdf/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtkoggtheora/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/include/vtk-8.1/vtkglew/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/llvm-3.3-0/lib/clang/3.3/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/llvm-3.3-0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/clang/3.3/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/glib-2.0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/dbus-1.0/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/wx/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/core/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtkglew/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtknetcdf/include")
prepend_path("FPATH",              "%{_prefix}/fslpython/envs/fslpython/include/vtk-8.1/vtkoggtheora/include")
prepend_path("FPATH",              "%{_prefix}/include")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ca-certificates-2018.03.07-0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/conda-env-2.6.0-1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/share/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libstdcxx-ng-8.2.0-hdf63c60_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/share/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/share/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/certifi-2018.8.24-py37_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/chardet-3.0.4-py37_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/idna-2.7-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pycosat-0.6.3-py37h14c3975_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pycparser-2.18-py37_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pysocks-1.6.8-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ruamel_yaml-0.15.46-py37h14c3975_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/six-1.11.0-py37_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py37he75722e_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/setuptools-40.2.0-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py37hc365091_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/wheel-0.31.1-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pip-10.0.1-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyopenssl-18.0.0-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/urllib3-1.23-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/requests-2.19.1-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/conda-4.5.11-py37_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/nibabel-2.2.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/idna-2.7-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/certifi-2018.10.15-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/mccabe-0.6.1-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/traitlets-4.3.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/msgpack-python-0.5.6-py36h6bb024c_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/dask-core-1.0.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/isodate-0.5.4-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/bokeh-1.0.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pynacl-1.3.0-py36h7b6447c_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cycler-0.10.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/wheel-0.32.3-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/future-0.17.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pycodestyle-2.3.1-py36hf609f19_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libgfortran-ng-7.3.0-hdf63c60_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/imageio-2.4.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/scipy-1.0.0-py36hbf646e7_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/heapdict-1.0.0-py36_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/psutil-5.4.8-py36h7b6447c_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyflakes-1.6.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/python-dateutil-2.7.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/lxml-4.1.1-py36hf71bdeb_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/docopt-0.6.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/distributed-1.25.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/packaging-18.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cloudpickle-0.6.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/blas-1.0-mkl/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pywavelets-1.0.1-py36hdd07704_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pytz-2018.7-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/sortedcontainers-2.1.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pylint-1.8.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/prompt_toolkit-1.0.15-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ptyprocess-0.6.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/llvm-3.3-0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/locket-0.2.0-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pypdf2-1.26.0-py_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/scikit-learn-0.19.1-py36hedc7406_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/toolz-0.9.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/system-5.8-2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ipython_genutils-0.2.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/networkx-1.11-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/mkl-service-1.1.2-py36h90e4bf4_5/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pygments-2.2.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/tbb-2019.1-hfd86e86_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/lazy-object-proxy-1.3.1-py36h14c3975_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/seaborn-0.8.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/astroid-1.6.5-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/matplotlib-2.1.1-py36ha26af80_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/dask-1.0.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py36he75722e_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/patsy-0.5.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyyaml-3.13-py36h14c3975_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pickleshare-0.7.5-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/tblib-1.3.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cytoolz-0.9.0.1-py36h14c3975_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/setuptools-40.6.2-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/h5py-2.8.0-py36h39dcb92_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/fslpy-1.12.0-pyh24bf2e0_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/mkl-2018.0.3-1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyqt-5.6.0-py36h22d08a2_6/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/wrapt-1.10.11-py36h14c3975_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/six-1.11.0-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/markupsafe-1.1.0-py36h7b6447c_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/tornado-5.1.1-py36h7b6447c_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/eddy_qc-1.0.0-py_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/intel-openmp-2019.1-144/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pandas-0.22.0-py36hf484d3e_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/deprecation-1.2-py_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/zict-0.1.3-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/jinja2-2.8.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/isort-4.3.4-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/scikit-image-0.13.1-py36h14c3975_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyparsing-2.2.0-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/simplegeneric-0.8.1-py36_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pydicom-1.2.1-py_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pexpect-4.6.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pyasn1-0.4.4-py36h28b3542_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/click-7.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pycparser-2.19-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/wcwidth-0.1.7-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/decorator-4.3.0-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pillow-5.0.0-py36h3deb7b8_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/flake8-3.5.0-py36_1/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/statsmodels-0.9.0-py36h035aef0_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py36hc365091_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/partd-0.3.9-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/paramiko-2.4.0-py36hd285e23_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/olefile-0.46-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/bcrypt-3.1.4-py36h14c3975_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/pkgs/pip-18.1-py36_0/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/share/info")
prepend_path("INFOPATH",           "%{_prefix}/fslpython/envs/fslpython/share/info")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/bin/FSLeyes/notebook/static/components/marked/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/bin/FSLeyes/notebook/static/components/codemirror/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/bin/FSLeyes/notebook/static/components/text-encoding/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/bin/FSLeyes/IPython/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/bin/FSLeyes/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/extras/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/extras/include/boost/tools/build/test/project-test3/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/extras/include/boost/tools/build/test/project-test4/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libstdcxx-ng-8.2.0-hdf63c60_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libstdcxx-ng-8.2.0-hdf63c60_1/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/certifi-2018.8.24-py37_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/chardet-3.0.4-py37_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/idna-2.7-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pycosat-0.6.3-py37h14c3975_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pycparser-2.18-py37_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pysocks-1.6.8-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ruamel_yaml-0.15.46-py37h14c3975_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/six-1.11.0-py37_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py37he75722e_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/setuptools-40.2.0-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py37hc365091_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wheel-0.31.1-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pip-10.0.1-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyopenssl-18.0.0-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/urllib3-1.23-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/requests-2.19.1-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/conda-4.5.11-py37_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/nibabel-2.2.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/idna-2.7-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/certifi-2018.10.15-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/mccabe-0.6.1-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/traitlets-4.3.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/msgpack-python-0.5.6-py36h6bb024c_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/dask-core-1.0.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/isodate-0.5.4-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/bokeh-1.0.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pynacl-1.3.0-py36h7b6447c_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cycler-0.10.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wheel-0.32.3-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/future-0.17.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pycodestyle-2.3.1-py36hf609f19_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libgfortran-ng-7.3.0-hdf63c60_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libgfortran-ng-7.3.0-hdf63c60_0/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/imageio-2.4.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/scipy-1.0.0-py36hbf646e7_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/heapdict-1.0.0-py36_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/psutil-5.4.8-py36h7b6447c_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyflakes-1.6.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/python-dateutil-2.7.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib/python3.6/site-packages/wx/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/lxml-4.1.1-py36hf71bdeb_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/core/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/docopt-0.6.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/distributed-1.25.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/packaging-18.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cloudpickle-0.6.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pywavelets-1.0.1-py36hdd07704_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pytz-2018.7-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/sortedcontainers-2.1.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pylint-1.8.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/prompt_toolkit-1.0.15-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ptyprocess-0.6.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/llvm-3.3-0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/locket-0.2.0-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/scikit-learn-0.19.1-py36hedc7406_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/toolz-0.9.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/system-5.8-2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ipython_genutils-0.2.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/networkx-1.11-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/mkl-service-1.1.2-py36h90e4bf4_5/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pygments-2.2.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/tbb-2019.1-hfd86e86_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/lazy-object-proxy-1.3.1-py36h14c3975_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/seaborn-0.8.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/astroid-1.6.5-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/matplotlib-2.1.1-py36ha26af80_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py36he75722e_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/lib/python3.6/site-packages/IPython/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/patsy-0.5.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyyaml-3.13-py36h14c3975_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pickleshare-0.7.5-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/tblib-1.3.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cytoolz-0.9.0.1-py36h14c3975_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/setuptools-40.6.2-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/h5py-2.8.0-py36h39dcb92_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/mkl-2018.0.3-1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyqt-5.6.0-py36h22d08a2_6/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wrapt-1.10.11-py36h14c3975_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/six-1.11.0-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/markupsafe-1.1.0-py36h7b6447c_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/tornado-5.1.1-py36h7b6447c_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/intel-openmp-2019.1-144/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pandas-0.22.0-py36hf484d3e_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/zict-0.1.3-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/jinja2-2.8.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/isort-4.3.4-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/scikit-image-0.13.1-py36h14c3975_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyparsing-2.2.0-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/simplegeneric-0.8.1-py36_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pexpect-4.6.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pyasn1-0.4.4-py36h28b3542_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/click-7.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pycparser-2.19-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/wcwidth-0.1.7-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/decorator-4.3.0-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pillow-5.0.0-py36h3deb7b8_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/flake8-3.5.0-py36_1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/statsmodels-0.9.0-py36h035aef0_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py36hc365091_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/partd-0.3.9-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/paramiko-2.4.0-py36hd285e23_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/olefile-0.46-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/bcrypt-3.1.4-py36h14c3975_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/pkgs/pip-18.1-py36_0/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/core/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/wx/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/IPython/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/fslpython/envs/fslpython/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/bin/FSLeyes/notebook/static/components/marked/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/bin/FSLeyes/notebook/static/components/codemirror/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/bin/FSLeyes/notebook/static/components/text-encoding/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/bin/FSLeyes/IPython/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/bin/FSLeyes/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/extras/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/extras/include/boost/tools/build/test/project-test3/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/extras/include/boost/tools/build/test/project-test4/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libgcc-ng-8.2.0-hdf63c60_1/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libstdcxx-ng-8.2.0-hdf63c60_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libstdcxx-ng-8.2.0-hdf63c60_1/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/certifi-2018.8.24-py37_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/chardet-3.0.4-py37_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/idna-2.7-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pycosat-0.6.3-py37h14c3975_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pycparser-2.18-py37_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pysocks-1.6.8-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ruamel_yaml-0.15.46-py37h14c3975_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/six-1.11.0-py37_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py37he75722e_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/setuptools-40.2.0-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py37hc365091_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wheel-0.31.1-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pip-10.0.1-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyopenssl-18.0.0-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/urllib3-1.23-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/requests-2.19.1-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/conda-4.5.11-py37_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/nibabel-2.2.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/idna-2.7-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/certifi-2018.10.15-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/mccabe-0.6.1-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/traitlets-4.3.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/msgpack-python-0.5.6-py36h6bb024c_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/dask-core-1.0.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/isodate-0.5.4-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/bokeh-1.0.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pynacl-1.3.0-py36h7b6447c_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cycler-0.10.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wheel-0.32.3-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/future-0.17.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pycodestyle-2.3.1-py36hf609f19_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libgfortran-ng-7.3.0-hdf63c60_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libgfortran-ng-7.3.0-hdf63c60_0/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/imageio-2.4.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/scipy-1.0.0-py36hbf646e7_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/heapdict-1.0.0-py36_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/psutil-5.4.8-py36h7b6447c_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyflakes-1.6.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/python-dateutil-2.7.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib/python3.6/site-packages/wx/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/lxml-4.1.1-py36hf71bdeb_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages/numpy/core/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/docopt-0.6.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/distributed-1.25.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/packaging-18.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cloudpickle-0.6.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pywavelets-1.0.1-py36hdd07704_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pytz-2018.7-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/sortedcontainers-2.1.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pylint-1.8.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/prompt_toolkit-1.0.15-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ptyprocess-0.6.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/llvm-3.3-0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/locket-0.2.0-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/scikit-learn-0.19.1-py36hedc7406_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/toolz-0.9.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/system-5.8-2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ipython_genutils-0.2.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/networkx-1.11-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/mkl-service-1.1.2-py36h90e4bf4_5/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pygments-2.2.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/tbb-2019.1-hfd86e86_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/lazy-object-proxy-1.3.1-py36h14c3975_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/seaborn-0.8.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/astroid-1.6.5-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/matplotlib-2.1.1-py36ha26af80_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py36he75722e_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/lib/python3.6/site-packages/IPython/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/patsy-0.5.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyyaml-3.13-py36h14c3975_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pickleshare-0.7.5-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/tblib-1.3.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cytoolz-0.9.0.1-py36h14c3975_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/setuptools-40.6.2-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/h5py-2.8.0-py36h39dcb92_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/mkl-2018.0.3-1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyqt-5.6.0-py36h22d08a2_6/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wrapt-1.10.11-py36h14c3975_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/six-1.11.0-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/markupsafe-1.1.0-py36h7b6447c_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/tornado-5.1.1-py36h7b6447c_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/intel-openmp-2019.1-144/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/hdf5-1.8.18-h6792536_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pandas-0.22.0-py36hf484d3e_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/zict-0.1.3-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/jinja2-2.8.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/isort-4.3.4-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/scikit-image-0.13.1-py36h14c3975_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyparsing-2.2.0-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/simplegeneric-0.8.1-py36_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pexpect-4.6.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pyasn1-0.4.4-py36h28b3542_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/click-7.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pycparser-2.19-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/wcwidth-0.1.7-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/decorator-4.3.0-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pillow-5.0.0-py36h3deb7b8_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/flake8-3.5.0-py36_1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/statsmodels-0.9.0-py36h035aef0_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py36hc365091_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/partd-0.3.9-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/paramiko-2.4.0-py36hd285e23_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/olefile-0.46-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/bcrypt-3.1.4-py36h14c3975_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/pkgs/pip-18.1-py36_0/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/core/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/numpy/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/wx/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages/IPython/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/fslpython/envs/fslpython/x86_64-conda_cos6-linux-gnu/sysroot/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("MANPATH",            "%{_prefix}/extras/share/man")
prepend_path("MANPATH",            "%{_prefix}/extras/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/ssl/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/readline-7.0-h7b6447c_5/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/llvm-3.3-0/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/jpeg-9b-h024ee3a_2/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/share/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/ssl/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/envs/fslpython/ssl/man")
prepend_path("MANPATH",            "%{_prefix}/fslpython/envs/fslpython/share/man")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/extras/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libffi-3.2.1-hd88cf55_4/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/ncurses-6.1-hf484d3e_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/openssl-1.0.2p-h14c3975_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/xz-5.2.4-h14c3975_4/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/yaml-0.1.7-had09818_2/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/zlib-1.2.11-ha838bed_2/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libedit-3.1.20170329-h6b74fdf_2/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/tk-8.6.8-hbc83047_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/sqlite-3.24.0-h84994c4_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/mesa-10.5.4-0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/zlib-1.2.11-h7b6447c_3/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/glib-2.53.6-h5d9569c_2/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/freetype-2.8-hab7d2ae_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/dbus-1.13.2-hc3f9b76_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libglu-9.0.0-hf484d3e_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/sqlite-3.25.3-h7b6447c_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/ncurses-6.1-he6710b0_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/expat-2.2.6-he6710b0_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/jsoncpp-1.8.3-h3a67955_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libxslt-1.1.32-h1312cb7_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/pcre-8.42-h439df22_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/fontconfig-2.12.6-h49f89f6_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/qt-5.6.2-hd25b39d_14/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/icu-58.2-h9c2bf20_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libxml2-2.9.8-h26e45fe_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libsodium-1.0.16-h1bed415_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libxcb-1.13-h1bed415_1/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/gstreamer-1.12.4-hb53b477_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libpng-1.6.35-hbc83047_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/libtiff-4.0.9-he85c1e1_2/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/pkgs/gst-plugins-base-1.12.4-h33fb286_0/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/lib/pkgconfig")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/fslpython/envs/fslpython/lib/pkgconfig")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/python-3.7.0-hc3d631a_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/certifi-2018.8.24-py37_1/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/chardet-3.0.4-py37_1/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/idna-2.7-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pycosat-0.6.3-py37h14c3975_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pycparser-2.18-py37_1/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pysocks-1.6.8-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/ruamel_yaml-0.15.46-py37h14c3975_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/six-1.11.0-py37_1/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py37he75722e_1/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/setuptools-40.2.0-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py37hc365091_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/wheel-0.31.1-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pip-10.0.1-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyopenssl-18.0.0-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/urllib3-1.23-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/requests-2.19.1-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/conda-4.5.11-py37_0/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/nibabel-2.2.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/idna-2.7-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/certifi-2018.10.15-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/mccabe-0.6.1-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/traitlets-4.3.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/msgpack-python-0.5.6-py36h6bb024c_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/dask-core-1.0.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/isodate-0.5.4-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/bokeh-1.0.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pynacl-1.3.0-py36h7b6447c_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cycler-0.10.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/wheel-0.32.3-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/future-0.17.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pycodestyle-2.3.1-py36hf609f19_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/imageio-2.4.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/scipy-1.0.0-py36hbf646e7_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/heapdict-1.0.0-py36_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/python-3.6.4-hc3d631a_3/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/psutil-5.4.8-py36h7b6447c_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyflakes-1.6.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/python-dateutil-2.7.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/wxpython-4.0.3-py36h2f155c4_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/lxml-4.1.1-py36hf71bdeb_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/numpy-1.14.0-py36ha266831_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/docopt-0.6.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/distributed-1.25.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/packaging-18.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cloudpickle-0.6.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/vtk-8.1.0-py36h9686630_201/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pywavelets-1.0.1-py36hdd07704_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pytz-2018.7-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/sortedcontainers-2.1.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pylint-1.8.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/prompt_toolkit-1.0.15-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/ptyprocess-0.6.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/locket-0.2.0-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pypdf2-1.26.0-py_2/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/scikit-learn-0.19.1-py36hedc7406_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/toolz-0.9.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/ipython_genutils-0.2.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/sip-4.18.1-py36hf484d3e_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/networkx-1.11-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/mkl-service-1.1.2-py36h90e4bf4_5/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pygments-2.2.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/lazy-object-proxy-1.3.1-py36h14c3975_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/seaborn-0.8.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/astroid-1.6.5-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/matplotlib-2.1.1-py36ha26af80_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cffi-1.11.5-py36he75722e_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/ipython-5.1.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/patsy-0.5.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyyaml-3.13-py36h14c3975_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pickleshare-0.7.5-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/tblib-1.3.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cytoolz-0.9.0.1-py36h14c3975_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/setuptools-40.6.2-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/h5py-2.8.0-py36h39dcb92_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/fslpy-1.12.0-pyh24bf2e0_1/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyqt-5.6.0-py36h22d08a2_6/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/wrapt-1.10.11-py36h14c3975_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/six-1.11.0-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/markupsafe-1.1.0-py36h7b6447c_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/asn1crypto-0.24.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/tornado-5.1.1-py36h7b6447c_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/eddy_qc-1.0.0-py_0/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pandas-0.22.0-py36hf484d3e_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/deprecation-1.2-py_0/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/zict-0.1.3-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/jinja2-2.8.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/isort-4.3.4-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/scikit-image-0.13.1-py36h14c3975_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyparsing-2.2.0-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/simplegeneric-0.8.1-py36_2/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pydicom-1.2.1-py_0/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pexpect-4.6.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pyasn1-0.4.4-py36h28b3542_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/click-7.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pycparser-2.19-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/wcwidth-0.1.7-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/decorator-4.3.0-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pillow-5.0.0-py36h3deb7b8_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/flake8-3.5.0-py36_1/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/statsmodels-0.9.0-py36h035aef0_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/cryptography-2.3.1-py36hc365091_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/partd-0.3.9-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/paramiko-2.4.0-py36hd285e23_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/olefile-0.46-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/bcrypt-3.1.4-py36h14c3975_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/pkgs/pip-18.1-py36_0/lib/python3.6/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/lib/python3.7/site-packages")
prepend_path("PYTHONPATH",         "%{_prefix}/fslpython/envs/fslpython/lib/python3.6/site-packages")

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
