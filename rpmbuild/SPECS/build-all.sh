#!/bin/bash

module purge
# read -a specs <<< "zlib-1.2.8-fasrc03 openmpi-1.8.1-fasrc04 mvapich2-2.0-fasrc02 gsl-1.16-fasrc03 expat-2.1.0-fasrc02 perl-5.10.1-fasrc03 perl-modules-5.10.1-fasrc09 boost-1.55.0-fasrc02"
# read -a specs <<< "boost-1.55.0-fasrc02 boost-1.54.0-fasrc02 boost-1.50.0-fasrc02 boost-1.41.0-fasrc02 boost-1.40.0-fasrc02"
# read -a specs <<< "boost-1.40.0-fasrc02"
# read -a specs <<< "beagle-2.1.trunk-fasrc02 htslib-1.1-fasrc02 samtools-0.1.17-fasrc02 samtools-0.1.19-fasrc02 samtools-1.1-fasrc03"
# read -a specs <<< "netcdf-3.6.3-fasrc02 blitz-0.10-fasrc02 bmtools-3.101-fasrc02 bwa-0.7.9a-fasrc02 cfitsio-3360-fasrc03 bcftools-1.0-fasrc02"
#read -a specs <<< "gmp-6.0.0-fasrc03"
# read -a specs <<< "mpfr-3.1.2-fasrc03"
# read -a specs <<< "ImageMagick-6.8.8-fasrc02 mpc-0.8.2-fasrc03"
# read -a specs <<< "ImageMagick-6.8.8-fasrc02"
#read -a specs <<< "mpc-1.0.2-fasrc02 ncbi-blast-2.2.29+-fasrc02  SuiteSparse-3.7.1-fasrc02  SuiteSparse-4.2.1-fasrc02 sparsehash-2.0.2-fasrc01"
# read -a specs <<< "sparsehash-2.0.2-fasrc02 ncbi-blast-2.2.29+-fasrc02" 
# Need to fix the spec name parsing so that dash in ncbi-blast is not converted
# read -a specs <<< "ncbi-blast-2.2.29+-fasrc02" 
# read -a specs <<< "beagle-2.1.trunk-fasrc02 htslib-1.1-fasrc02 samtools-0.1.17-fasrc02 samtools-0.1.19-fasrc02"
# read -a specs <<< "beagle-2.1.trunk-fasrc02 samtools-0.1.17-fasrc02 samtools-0.1.19-fasrc02"
#read -a specs <<< "oases-0.2.08-fasrc02 velvet-1.2.10-fasrc02 openexr-2.2.0-fasrc02 variscan-2.0.3-fasrc02 stacks-1.19-fasrc03"
#read -a specs <<< "Healpix-3.11-fasrc03 MUMmer-3.23-fasrc02 PolSpice-v03.00.01-fasrc02 arprec-2.2.17-fasrc02 autodocksuite-4.2.5.1-fasrc02 paml-4.8-fasrc02"
# read -a specs <<< "oases-0.2.08-fasrc02 arprec-2.2.17-fasrc02 OpenMM-6.1-fasrc02"

# Could not get this to work with Intel
#read -a specs <<< "OpenMM-6.0.1-fasrc02"
#read -a specs <<< ""
#read -a specs <<< "beagle-2.1.trunk-fasrc02"
#read -a specs <<< "gsl-1.16-fasrc03"

#read -a specs <<< "OpenMM-6.0.1-fasrc02"

#read -a specs <<< "blitz-0.10-fasrc02"
#read -a specs <<< "gd-2.0.28-fasrc01"
read -a specs <<< "blitz-0.10-fasrc02 variscan-2.0.3-fasrc02"

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

# Dash in the name
#export NAME=perl-modules
#export VERSION=5.10.1
#export RELEASE=fasrc09
#export TYPE=Comp 
#echo "NAME $NAME, VERSION $VERSION, RELEASE $RELEASE"
#make && make install

#read -a specs <<< "hdf5-1.8.12-fasrc05"
#read -a specs <<< "netcdf-4.3.2-fasrc03"
#read -a specs <<< "netcdf-fortran-4.4.0-fasrc03 libcircle-0.2.0.rc.1-fasrc03 libdftw-0.0.2-fasrc02 Amber-14-fasrc02 autodocksuite-4.2.5.1-fasrc02"
#read -a specs <<< "raxml-8.1.5-fasrc02 freefem++-3.31.2-fasrc02 esmf-6.3.0r-fasrc02 ExaML-2.0.4-fasrc02 fsmr-0.0.1-fasrc02 mrbayes-3.2.3-fasrc02 mrmpi-7Apr14-fasrc02 pb_mpi-1.5a-fasrc02"

#read -a specs <<< "relion-1.3-fasrc02"
#read -a specs <<< "raxml-8.1.5-fasrc02 freefem++-3.31.2-fasrc02 esmf-6.3.0r-fasrc02 fsmr-0.0.1-fasrc02 mrbayes-3.2.3-fasrc02 mrmpi-7Apr14-fasrc02"

#read -a specs <<< "fftw-3.3.4-fasrc06"
#read -a specs <<< "raxml-8.1.5-fasrc02 freefem++-3.31.2-fasrc02 esmf-6.3.0r-fasrc02 fsmr-0.0.1-fasrc02 mrbayes-3.2.3-fasrc02"
#read -a specs <<< "freefem++-3.31.2-fasrc02 esmf-6.3.0r-fasrc02 fsmr-0.0.1-fasrc02 mrbayes-3.2.3-fasrc02"
#read -a specs <<< "libcircle-0.2.0.rc.1-fasrc03"
#read -a specs <<< "freefem++-3.31.2-fasrc02 esmf-6.3.0r-fasrc02 fsmr-0.0.1-fasrc02 mrbayes-3.2.3-fasrc02"
#read -a specs <<< "freefem++-3.31.2-fasrc02 fsmr-0.0.1-fasrc02"
#read -a specs <<< "libdftw-0.0.2-fasrc02"

#Couldn't get this to work.  freefem/src/lglib won't build.
#read -a specs <<< "freefem++-3.31.2-fasrc02 fsmr-0.0.1-fasrc02"

#Had to remove the intel include paths from CPATH
#read -a specs <<< "eman2-2.0RC3-fasrc02"
#read -a specs <<< "freefem++-3.31.2-fasrc02"
#read -a specs <<< "lammps-28Jun14-fasrc04"
#read -a specs <<< "fftw-2.1.5-fasrc03"
#read -a specs <<< "lammps-28Jun14-fasrc04"
#read -a specs <<< "gromacs-5.0-fasrc02f"
#read -a specs <<< "eman2-2.0RC3-fasrc02"
#read -a specs <<< "netcdf-4.1.3-fasrc02 BayesPhylogenies-2.0.2-fasrc02"
#read -a specs <<< "netcdf-4.1.3-fasrc02"
read -a specs <<< ""


for spec in "${specs[@]}"
do
    echo "Spec '$spec'"
    if [ -n "$spec" ]
    then
        arr=(`echo $spec | tr "-" "\n"`)
        export NAME=${arr[0]}
        export VERSION=${arr[1]}
        export RELEASE=${arr[2]}
        export TYPE=MPI 
        echo "NAME $NAME, VERSION $VERSION, RELEASE $RELEASE"
        make && make install
    fi
done

# Dash in netcdf-fortran
#export NAME=netcdf-fortran
#export VERSION=4.4.0
#export RELEASE=fasrc02
#export TYPE=MPI 
#echo "NAME $NAME, VERSION $VERSION, RELEASE $RELEASE"
#make && make install
