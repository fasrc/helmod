fasrcsw is a software management system where:

* apps are built, packaged, and installed using [RPM](http://www.rpm.org/)
* each app is installed under its own relocatable prefix
* software environments are managed with [Lmod](http://www.tacc.utexas.edu/tacc-projects/lmod)
* it's easy to manage entire software environments for multiple compiler and MPI implementations

See the `doc` directory for more information, specifically:

* [INSTALL](doc/INSTALL.md) for initial installation and setup
* [HOWTO](doc/HOWTO.md) for day-to-day usage instructions (or [HOWTO-short](doc/HOWTO-short.md) for experienced users)
* [FAQ](doc/FAQ.md) for answers to common questions and other details

fasrcsw captures all the details and hacks that go into building any given software package as as shell snippets in RPM spec files.
See the [rpmbuild/SPECS](rpmbuild/SPECS) directory for a bunch of examples (see [this FAQ item](doc/FAQ.md#how-do-i-diff-a-spec-file-with-the-relevant-version-of-the-template-spec-file) for diffing them from the template for the interesting bits).
