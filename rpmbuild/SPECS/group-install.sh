#!/bin/env bash

export TYPE=Comp
export NAME=szip
export VERSION=2.1
export RELEASE=fasrc02
make 
make install
make publish

export TYPE=Comp
export NAME=zlib
export VERSION=1.2.8
export RELEASE=fasrc07
make
make install
make publish

export TYPE=MPI
export NAME=hdf5
export VERSION=1.8.12
export RELEASE=fasrc12
make 
make install
make publish

export TYPE=MPI
export NAME=hdf5
export VERSION=1.10.1
export RELEASE=fasrc01
make 
make install
make publish

export TYPE=MPI
export NAME=netcdf
export VERSION=4.1.3
export RELEASE=fasrc09
make 
make install
make publish

export TYPE=MPI
export NAME=netcdf
export VERSION=4.4.1.1
export RELEASE=fasrc02
make
make install
make publish

export TYPE=MPI
export NAME=netcdf-fortran
export VERSION=4.4.4
export RELEASE=fasrc05
make
make install
make publish
