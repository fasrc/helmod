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
%define summary_static Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine
Summary: %{summary_static}

#
# enter the url from where you got the source; change the archive suffix if 
# applicable
#
URL: https://nodejs.org/dist/v4.4.7/node-v4.4.7.tar.gz
Source: %{name}-v%{version}.tar.gz

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
# NOTE! INDICATE IF THERE ARE CHANGES FROM THE NORM TO THE BUILD!
#
%description
Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine. Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient. Node.js' package ecosystem, npm, is the largest ecosystem of open source libraries in the world.

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
rm -rf %{name}-v%{version}
tar xvf "$FASRCSW_DEV"/rpmbuild/SOURCES/%{name}-v%{version}.tar.*
cd %{name}-v%{version}
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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-v%{version}


./configure --prefix=%{_prefix}

#if you are okay with disordered output, add %%{?_smp_mflags} (with only one 
#percent sign) to build in parallel
make



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
cd "$FASRCSW_DEV"/rpmbuild/BUILD/%{name}-v%{version}
echo %{buildroot} | grep -q %{name}-v%{version} && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}
make install DESTDIR=%{buildroot}


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
setenv("NODE_HOME",       "%{_prefix}")
setenv("NODE_PATH",       "%{_prefix}/bin")
setenv("NODE_INCLUDE",    "%{_prefix}/include")
setenv("NODE_LIB",        "%{_prefix}/lib")

prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/semver/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/mkdirp/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/nopt/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/which/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/har-validator/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/node-uuid/bin")
prepend_path("PATH",               "%{_prefix}/lib/node_modules/npm/bin")
prepend_path("PATH",               "%{_prefix}/bin")
prepend_path("CPATH",              "%{_prefix}/include")
prepend_path("FPATH",              "%{_prefix}/include")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/retry/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/slide/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/read/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/fstream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/readable-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/ansi/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/sorted-object/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/path-is-inside/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/retry/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/concat-stream/node_modules/readable-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/concat-stream/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/read-package-json/node_modules/json-parse-helpfulerror/node_modules/jju/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/node_modules/minimatch/node_modules/lru-cache/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/nopt/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/normalize-package-data/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/sha/node_modules/readable-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/sha/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/hoek/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/sntp/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/cryptiles/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/boom/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/har-validator/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/qs/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/form-data/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/form-data/node_modules/async/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/combined-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/combined-stream/node_modules/delayed-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/verror/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/json-schema/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/extsprintf/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/getpass/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/ecc-jsbn/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/asn1/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/jodid25519/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/dashdash/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/bl/node_modules/readable-stream/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/bl/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/tough-cookie/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/lru-cache/lib")
prepend_path("LD_LIBRARY_PATH",    "%{_prefix}/lib/node_modules/npm/node_modules/tar/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/retry/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/slide/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/read/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/fstream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/readable-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/ansi/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/sorted-object/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/path-is-inside/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/retry/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/concat-stream/node_modules/readable-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/concat-stream/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/read-package-json/node_modules/json-parse-helpfulerror/node_modules/jju/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/node-gyp/node_modules/minimatch/node_modules/lru-cache/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/nopt/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/normalize-package-data/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/sha/node_modules/readable-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/sha/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/hoek/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/sntp/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/cryptiles/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/boom/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/har-validator/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/qs/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/form-data/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/form-data/node_modules/async/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/combined-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/combined-stream/node_modules/delayed-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/verror/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/json-schema/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/extsprintf/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/getpass/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/ecc-jsbn/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/asn1/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/jodid25519/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/dashdash/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/bl/node_modules/readable-stream/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/bl/node_modules/readable-stream/node_modules/core-util-is/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/tough-cookie/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/lru-cache/lib")
prepend_path("LIBRARY_PATH",       "%{_prefix}/lib/node_modules/npm/node_modules/tar/lib")
prepend_path("MANPATH",            "%{_prefix}/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/man")
prepend_path("MANPATH",            "%{_prefix}/lib/node_modules/npm/man")
prepend_path("MANPATH",            "%{_prefix}/share/man")
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
