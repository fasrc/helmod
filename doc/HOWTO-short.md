__cd__ to your personal *fasrcsw* clone (on the canonical build host, as you, not root), and get setup:

``` bash
git pull
module purge
source ./setup.sh
```

__download__ the source archive to `"$FASRCSW_DEV"/rpmbuild/SOURCES`

__define__ what you're working on (`TYPE` is `Comp` for generic things, `MPI` for MPI-enabled things):

``` bash
export NAME=...
export VERSION=...
export RELEASE=...
export TYPE=...
```

__create__ a spec file:

``` bash
cd "$FASRCSW_DEV"/rpmbuild/SPECS
cp -ai template.spec "$NAME-$VERSION-$RELEASE".spec
```

__edit__ the spec file and __address__ each `FIXME` up until the modulefile.lua creation

do a __trial build__:

``` bash
make trial
```

__finish__ the spec file (modulefile.lua creation), based upon the suggestions in the output from the above.

__build__ it for real:

``` bash
make
```

__install__ it:

``` bash
make test
make install
```

__commit/post__ your updates:

``` bash
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SOURCES/
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/RPMS/
sudo rsync -avu {"$FASRCSW_DEV","$FASRCSW_PROD"}/rpmbuild/SRPMS/
cd "$FASRCSW_DEV"
```

``` bash
cd "$FASRCSW_DEV"
git add .
git commit -v .
git pull
git push
```
