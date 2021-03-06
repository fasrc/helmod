.PHONY: all trial build filelist filequery test install query post uninstall publish

all: build

trial:
	fasrcsw-rpmbuild-$$TYPE --define 'trial yes' -ba "$$NAME-$$VERSION-$$RELEASE".spec

build:
	fasrcsw-rpmbuild-$$TYPE -ba "$$NAME-$$VERSION-$$RELEASE".spec

filelist:
	fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE"

filequery:
	fasrcsw-rpm -qilp $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE")

test:
	sudo -E fasrcsw-rpm -ivh --oldpackage --nodeps --test $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE")

install: 
	sudo -E fasrcsw-rpm -ivh --nofiledigest --oldpackage --nodeps $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE")
	sudo -E fasrcsw-update-lmod-spider-cache
	sudo -E chmod 644 "$$FASRCSW_PROD"/moduledata/cacheDir/*

query:
	fasrcsw-rpm -qa | grep "^$$NAME-$$VERSION-$$RELEASE" || true

sync:
	sudo rsync -auv {"$$FASRCSW_DEV","$$FASRCSW_PROD"}/rpmbuild/SOURCES/
	sudo rsync -auv {"$$FASRCSW_DEV","$$FASRCSW_PROD"}/rpmbuild/RPMS/
	sudo rsync -auv {"$$FASRCSW_DEV","$$FASRCSW_PROD"}/rpmbuild/SRPMS/

post: sync
	cd "$$FASRCSW_DEV"
	git add --all .
	git commit -m "added new software".
	git pull
	git push

uninstall: 
	sudo -E fasrcsw-rpm -ev --nodeps $$(fasrcsw-list-$$TYPE-rpms "$$NAME-$$VERSION-$$RELEASE" | xargs -I% basename % .rpm)
	sudo -E fasrcsw-update-lmod-spider-cache
publish:
	PATH=/opt/builds/bin:$$PATH load-build "$${FASRCSW_DEV}/appdata/$$NAME-$$VERSION-$$RELEASE.$$TYPE.dat"
	PATH=/opt/builds/bin:$$PATH update-module-load $$FASRCSW_PROD/modulefiles
	sudo cp "$${FASRCSW_DEV}/appdata/$$NAME-$$VERSION-$$RELEASE.$$TYPE.dat" "$${FASRCSW_PROD}/appdata"
	sudo /usr/bin/loadBuild --flavor helmod "/n/sw/helmod/appdata/$$NAME-$$VERSION-$$RELEASE.$$TYPE.dat" 

alias:
	helmod-alias $$ALIAS

