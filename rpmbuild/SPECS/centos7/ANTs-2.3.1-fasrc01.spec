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
%define summary_static Advanced Normalization Tools (ANTs) 
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://github.com/ANTsX/ANTs/archive/v2.3.1.tar.gz
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


%define builddependencies cmake/3.12.1-fasrc01
%define rundependencies %{nil}
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
ANTs computes high-dimensional mappings to capture the statistics of brain structure and function.

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

rm -rf build
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} ../.

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel
make %{?_smp_mflags}

cp ../Scripts/* bin/.


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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}/build
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

cp -r * %{buildroot}/%{_prefix}
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
setenv("ANTs_HOME",       "%{_prefix}")
setenv("ANTSPATH",	  "%{_prefix}/bin/")
setenv("ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS", "1")

prepend_path("PATH",               "%{_prefix}/ITKv5-install/bin")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Bridge/NumPy/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Bridge/VTK/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Bridge/VtkGlue/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/Common/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/FiniteDifference/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/GPUCommon/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/GPUFiniteDifference/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/ImageAdaptors/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/ImageFunction/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/Mesh/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/QuadEdgeMesh/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/SpatialObjects/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/TestKernel/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Core/Transform/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/AnisotropicSmoothing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/AntiAlias/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/BiasCorrection/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/BinaryMathematicalMorphology/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Colormap/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Convolution/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/CurvatureFlow/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Deconvolution/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Denoising/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DiffusionTensorImage/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DisplacementField/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DistanceMap/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/FFT/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/FastMarching/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUAnisotropicSmoothing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUImageFilterBase/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUSmoothing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUThresholding/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageCompare/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageCompose/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFeature/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFilterBase/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFusion/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageGradient/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageGrid/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageIntensity/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageLabel/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageNoise/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageSources/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageStatistics/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/LabelMap/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/MathematicalMorphology/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Path/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/QuadEdgeMeshFiltering/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Smoothing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/SpatialFunction/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Thresholding/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/BMP/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/BioRad/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/Bruker/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/CSV/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/DCMTK/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/GDCM/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/GE/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/GIPL/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/HDF5/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/IPL/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/ImageBase/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/JPEG/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/LSM/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/MINC/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/MRC/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/Mesh/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshBYU/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshBase/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshVTK/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/Meta/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/NIFTI/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/NRRD/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/PNG/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/PhilipsREC/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/RAW/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/Siemens/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/SpatialObjects/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/Stimulate/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TIFF/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformBase/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformFactory/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformHDF5/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformInsightLegacy/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformMINC/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformMatlab/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/VTK/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/IO/XML/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Nonunit/Review/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Eigen/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/FEM/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/NarrowBand/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Optimizers/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Optimizersv4/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Polynomials/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Statistics/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/Common/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/FEM/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/GPUCommon/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/GPUPDEDeformable/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/Metricsv4/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/PDEDeformable/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Registration/RegistrationMethodsv4/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Remote/MGHIO/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Classifiers/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/ConnectedComponents/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/DeformableMesh/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/KLMRegionGrowing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LabelVoting/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSets/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSetsv4/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSetsv4Visualization/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/MarkovRandomFieldsClassifiers/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/RegionGrowing/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/SignedDistanceFunction/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Voronoi/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Watersheds/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/GoogleTest/src/itkgoogletest/googletest/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/KWIML/src/itkkwiml/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/VNLInstantiation/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/libLBFGS/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Video/BridgeOpenCV/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Video/BridgeVXL/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Video/Core/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Video/Filtering/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5/Modules/Video/IO/include")
prepend_path("CPATH",              "%{_prefix}/ITKv5-install/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Bridge/NumPy/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Bridge/VTK/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Bridge/VtkGlue/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/Common/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/FiniteDifference/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/GPUCommon/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/GPUFiniteDifference/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/ImageAdaptors/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/ImageFunction/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/Mesh/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/QuadEdgeMesh/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/SpatialObjects/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/TestKernel/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Core/Transform/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/AnisotropicSmoothing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/AntiAlias/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/BiasCorrection/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/BinaryMathematicalMorphology/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Colormap/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Convolution/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/CurvatureFlow/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Deconvolution/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Denoising/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DiffusionTensorImage/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DisplacementField/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/DistanceMap/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/FFT/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/FastMarching/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUAnisotropicSmoothing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUImageFilterBase/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUSmoothing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/GPUThresholding/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageCompare/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageCompose/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFeature/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFilterBase/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageFusion/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageGradient/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageGrid/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageIntensity/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageLabel/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageNoise/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageSources/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/ImageStatistics/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/LabelMap/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/MathematicalMorphology/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Path/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/QuadEdgeMeshFiltering/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Smoothing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/SpatialFunction/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Filtering/Thresholding/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/BMP/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/BioRad/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/Bruker/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/CSV/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/DCMTK/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/GDCM/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/GE/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/GIPL/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/HDF5/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/IPL/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/ImageBase/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/JPEG/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/LSM/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/MINC/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/MRC/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/Mesh/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshBYU/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshBase/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/MeshVTK/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/Meta/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/NIFTI/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/NRRD/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/PNG/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/PhilipsREC/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/RAW/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/Siemens/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/SpatialObjects/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/Stimulate/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TIFF/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformBase/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformFactory/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformHDF5/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformInsightLegacy/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformMINC/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/TransformMatlab/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/VTK/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/IO/XML/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Nonunit/Review/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Eigen/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/FEM/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/NarrowBand/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Optimizers/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Optimizersv4/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Polynomials/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Numerics/Statistics/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/Common/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/FEM/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/GPUCommon/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/GPUPDEDeformable/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/Metricsv4/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/PDEDeformable/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Registration/RegistrationMethodsv4/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Remote/MGHIO/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Classifiers/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/ConnectedComponents/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/DeformableMesh/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/KLMRegionGrowing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LabelVoting/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSets/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSetsv4/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/LevelSetsv4Visualization/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/MarkovRandomFieldsClassifiers/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/RegionGrowing/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/SignedDistanceFunction/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Voronoi/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Segmentation/Watersheds/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/GoogleTest/src/itkgoogletest/googletest/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/KWIML/src/itkkwiml/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/VNLInstantiation/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/ThirdParty/libLBFGS/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Video/BridgeOpenCV/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Video/BridgeVXL/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Video/Core/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Video/Filtering/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5/Modules/Video/IO/include")
prepend_path("FPATH",              "%{_prefix}/ITKv5-install/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ITKv5/Modules/ThirdParty/GDCM/src/gdcm/Utilities/gdcmopenjpeg/src/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ITKv5-build/CMakeFiles/Export/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ITKv5-build/Modules/ThirdParty/GDCM/src/gdcm/Utilities/gdcmopenjpeg/src/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ITKv5-build/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/ITKv5-install/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ITKv5/Modules/ThirdParty/GDCM/src/gdcm/Utilities/gdcmopenjpeg/src/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ITKv5-build/CMakeFiles/Export/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ITKv5-build/Modules/ThirdParty/GDCM/src/gdcm/Utilities/gdcmopenjpeg/src/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ITKv5-build/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/ITKv5-install/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("PKG_CONFIG_PATH",    "%{_prefix}/ITKv5-install/lib/pkgconfig")
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
