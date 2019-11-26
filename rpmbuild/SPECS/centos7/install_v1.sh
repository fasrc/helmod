#export NAME=openmpi VERSION=3.1.1 TYPE=Comp RELEASE=fasrc02
#make
#make install
#make publish

#export NAME=szip VERSION=2.1 TYPE=Comp RELEASE=fasrc03
#make
#make install
#make publish

#export NAME=zlib VERSION=1.2.11 TYPE=Comp RELEASE=fasrc02
#make
#make install
#make publish

#export NAME=hdf5 VERSION=1.10.5 TYPE=Comp RELEASE=fasrc03
#make
#make install
#make publish

#export NAME=netcdf VERSION=4.7.1 TYPE=Comp RELEASE=fasrc02
#make
#make install
#make publish

#export NAME=netcdf-fortran VERSION=4.5.2 TYPE=Comp RELEASE=fasrc02
#make
#make install
#make publish

export NAME=hdf5 VERSION=1.10.5 TYPE=MPI RELEASE=fasrc02
make
make install
make publish

export NAME=netcdf VERSION=4.7.1 TYPE=MPI RELEASE=fasrc01
make
make install
make publish

export NAME=netcdf-fortran VERSION=4.5.2 TYPE=MPI RELEASE=fasrc01
make
make install
make publish

