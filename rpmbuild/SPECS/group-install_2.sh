#!/bin/env bash
export TYPE=Comp
export NAME=gsl
export VERSION=2.3
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=OpenBLAS
export VERSION=0.2.18
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=armadillo
export VERSION=6.700.6
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=cfitsio
export VERSION=3390
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=openmpi
export VERSION=2.1.0
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=mvapich2
export VERSION=2.2
export RELEASE=fasrc01
make
make install
make publish

export TYPE=Comp
export NAME=mpich
export VERSION=3.2
export RELEASE=fasrc03
make
make install
make publish

