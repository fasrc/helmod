#!/bin/env bash
export TYPE=MPI
export NAME=hdf5
export VERSION=1.8.12
export RELEASE=fasrc12
make
make install
make publish

export TYPE=MPI
export NAME=hdf5
export VERSION=1.8.16
export RELEASE=fasrc03
make
make install
make publish

export TYPE=MPI
export NAME=hdf5
export VERSION=1.8.17
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
export VERSION=4.3.2
export RELEASE=fasrc05
make
make install
make publish

export TYPE=MPI
export NAME=netcdf
export VERSION=4.4.0
export RELEASE=fasrc02
make
make install
make publish

export TYPE=MPI
export NAME=netcdf-cxx
export VERSION=4.2
export RELEASE=fasrc03
make
make install
make publish

export TYPE=MPI
export NAME=netcdf-cxx4
export VERSION=4.2.1
export RELEASE=fasrc03
make
make install
make publish

export TYPE=MPI
export NAME=netcdf-fortran
export VERSION=4.4.3
export RELEASE=fasrc02
make
make install
make publish

export TYPE=MPI
export NAME=parallel-netcdf
export VERSION=1.8.1
export RELEASE=fasrc01
make
make install
make publish

