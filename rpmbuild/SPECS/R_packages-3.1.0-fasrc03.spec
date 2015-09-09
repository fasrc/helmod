#
# R_packages-3.1.0-fasrc01, with 192 packages built, takes about 40 minutes
#



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
%define summary_static a bunch of R packages from CRAN
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if
# applicable
#
#URL: http://...
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


%define builddependencies R_core/3.1.0-fasrc01
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
This is the set of most popular packages added on to R that originate from CRAN.
It's meant to be paired with an R_core module.



#------------------- %%prep (~ tar xvf) ---------------------------------------

%prep


#
# unpack the sources here.  The default below is for standard, GNU-toolchain
# style things -- hopefully it'll just work as-is.
#

umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}


#--- name all the packages to install
#
# this is the union of:
#	* what's in our old centos6/R-3.0.2 (most popular R module)
#	* what's in our old math/R-3.0.1 (2nd most popular R module)
#	* top 100 most popular packages by downloads for part of 2013:
#	  http://www.r-statistics.com/2013/06/top-100-r-packages-for-2013-jan-may/
#
# minus built-in stuff
#	KernSmooth
#	MASS
#	Matrix
#	base
#	boot
#	class
#	cluster
#	codetools
#	compiler
#	datasets
#	foreign
#	grDevices
#	graphics
#	grid
#	lattice
#	methods
#	mgcv
#	nlme
#	nnet
#	parallel
#	rpart
#	spatial
#	splines
#	stats
#	stats4
#	survival
#	tcltk
#	tools
#	utils
#
# minus these that failed (grepping output for `ERROR'):
#	RODBC
#	RWeka
#	RWekajars
#	RcppGSL
#	Rmpi
#	WGCNA
#	XLConnect
#	copula
#	diversitree
#	gsl
#	impute
#	isva
#	ncdf
#	qvalue
#	rJava
#	rgdal
#	topicmodels
#	xlsx
#	xlsxjars
#
# minus these that ended up not building (e.g. not in CRAN)
#	AnnotationDbi
#	BSgenome
#	BayesTree
#	Biobase
#	BiocGenerics
#	BiocInstaller
#	Biostrings
#	DESeq
#	DiffBind
#	GenomicFeatures
#	GenomicRanges
#	Gviz
#	IRanges
#	IlluminaHumanMethylation450kanno.ilmn12.hg19
#	Models
#	Proportional-Odds
#	Rsamtools
#	ShortRead
#	Snowball
#	XVector
#	annotate
#	biomaRt
#	biovizBase
#	bumphunter
#	ctc
#	cummeRbund
#	edgeR
#	genefilter
#	geneplotter
#	genomes
#	hopach
#	illuminaio
#	int64
#	limma
#	manipulate
#	marray
#	methylumi
#	minfi
#	multtest
#	pcaMethods
#	peer
#	preprocessCore
#	rstan
#	rstudio
#	rtracklayer
#	siggenes
#	slider
#	spp
#	zlibbioc
#
# and these packages show up, too (pulled in a dependencies I guess)
#	DEoptimR
#	Defaults
#	NLP
#	TH.data
#	expm
#	fastmatch
#	fracdiff
#	gss
#	highr
#	httr
#	mime
#	permute
#	tcltk2
#	whisker

cat > package_list <<EOF
ADGofTest
AnDE
BB
Brobdingnag
CpGassoc
DBI
FNN
Formula
GSA
GWAF
GenABEL
GenABEL.data
Hmisc
MCMCpack
MatchIt
MetaSKAT
R.methodsS3
R2WinBUGS
RColorBrewer
RCurl
RJSONIO
RSQLite
RSQLite.extfuns
RSiena
Rcmdr
Rcpp
RcppArmadillo
RcppEigen
Rserve
SKAT
SnowballC
SparseM
TTR
XML
abind
akima
amap
aod
ape
aplpack
arm
base64
bdsmatrix
beanplot
bitops
caTools
car
chron
coda
colorspace
corpcor
coxme
cubature
data.table
deSolve
devtools
dichromat
digest
discretization
doParallel
doRNG
doSNOW
dynamicTreeCut
e1071
effects
evaluate
fBasics
fastICA
fastcluster
fields
flashClust
foreach
forecast
formatR
formula.tools
functional
gamm4
gdata
geepack
ggplot2
glmnet
gplots
gridExtra
grplasso
gsubfn
gtable
gtools
hwriter
igraph
inline
intervals
iterators
itertools
kernlab
knitr
labeling
lasso2
latticeExtra
lda
leaps
lhs
lme4
lmtest
locfit
maps
maptools
markdown
matrixStats
matrixcalc
mclust
memoise
meta
mi
minqa
mlbench
mlegp
modeltools
msm
multcomp
multicore
munsell
mvtnorm
nleqslv
nor1mix
numDeriv
operator.tools
optmatch
pROC
penalized
penalizedSVM
phangorn
pkgmaker
plotrix
plyr
proto
pspline
psych
quadprog
quantmod
quantreg
rJava
randomForest
raster
registry
relimp
reshape
reshape2
rgl
rngtools
robustbase
rootSolve
sandwich
sas7bdat
scales
scatterplot3d
sem
slam
snow
sp
spam
sqldf
stabledist
statmod
stringr
strucchange
subplex
svmpath
texreg
tgp
timeDate
timeSeries
tm
tree
truncnorm
tseries
vcd
vegan
xtable
xts
zoo
RWekajars
RWeka
XLConnect
xlsx
xlsxjars
EOF



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

#(n/a -- build and install done in the same step below)



#------------------- %%install (~ make install + create modulefile) -----------

%install

#(leave this here)
%include fasrcsw_module_loads.rpmmacros


#
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


#
# This app insists* on writing directly to the prefix.  Acquiesce, and hack a
# symlink, IN THE PRODUCTION DESTINATION (yuck), back to our where we want it
# to install in our build environment, and then remove the symlink.  Note that
# this will only work for the first build of this NAME/VERSION/RELEASE/TYPE
# combination.
#
# * Well, with R here, maybe there's a way; I just don't know it.
#

# Standard stuff.
umask 022
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-%{version}
echo %{buildroot} | grep -q %{name}-%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}

# Make the symlink.
sudo mkdir -p "$(dirname %{_prefix})"
test -L "%{_prefix}" && sudo rm "%{_prefix}" || true

##can't use a symlink -- R canonicalizes it and includes the buildroot in the files
#sudo ln -s "%{buildroot}/%{_prefix}" "%{_prefix}"
sudo install -o "$USER" -m 700 -d "%{_prefix}"


echo 'install.packages(scan("package_list", what="", sep="\n"), lib="%{_prefix}", repos="http://cran.us.r-project.org")' | R --vanilla
#NOTE: some may fail
rm -rf %{buildroot}/%{_prefix}
mkdir -p %{buildroot}/%{_prefix}
cp -r "%{_prefix}"/* %{buildroot}/%{_prefix}

##can't use a symlink -- R canonicalizes it and includes the buildroot in the files
# Clean up the symlink.  (The parent dir may be left over, oh well.)
sudo rm -rf "%{_prefix}"


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
prepend_path("R_LIBS_USER",         "%{_prefix}")
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
