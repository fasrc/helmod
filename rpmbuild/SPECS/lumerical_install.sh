#!/bin/bash
for i in 8.6.3 8.5.4 8.0.4 7.5.1 7.5.0 6.5.8_nnin 6.5
do
    echo "version: $i"
    export VERSION=$i
    export TYPE=Core
    make uninstall
    export TYPE=MPI
    make
    make install
    echo "All done."
done
