.PHONY: all clean build install

all: clean build install

clean: 
	sudo -E fasrcsw-rpm -ev --nodeps $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE" | xargs -I% basename % .rpm)
	source /etc/profile.d/lmod.sh; module purge

trial:
	fasrcsw-rpmbuild-$$TYPE --define 'trial yes' -ba "$$NAME-$$VERSION-$$RELEASE".spec

build:
	fasrcsw-rpmbuild-$$TYPE -ba "$$NAME-$$VERSION-$$RELEASE".spec

install: 
	sudo -E fasrcsw-rpm -ivh --oldpackage --nodeps $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE")

test:
	sudo -E fasrcsw-rpm -ivh --oldpackage --nodeps --test $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE")
