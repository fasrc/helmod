#!/bin/bash

# read -a specs <<< "zlib-1.2.8-fasrc03 openmpi-1.8.1-fasrc04 mvapich2-2.0-fasrc02 gsl-1.16-fasrc03 expat-2.1.0-fasrc02 perl-5.10.1-fasrc03 perl-modules-5.10.1-fasrc09 boost-1.55.0-fasrc02"
read -a specs <<< "boost-1.55.0-fasrc02 boost-1.54.0-fasrc02 boost-1.50.0-fasrc02 boost-1.41.0-fasrc02 boost-1.40.0-fasrc02"

for spec in "${specs[@]}"
do
    echo "Spec '$spec'"
    if [ -n "$spec" ]
    then
        arr=(`echo $spec | tr "-" "\n"`)
        export NAME=${arr[0]}
        export VERSION=${arr[1]}
        export RELEASE=${arr[2]}
        export TYPE=Comp 
        echo "NAME $NAME, VERSION $VERSION, RELEASE $RELEASE"
        make && make install
    fi
done
