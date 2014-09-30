if [ "${FASRC_MODULE_FLAVOR:-}" != 'lmod' ]; then
	#in child shells after this has already been sourced, don't want to try to purge lmod modules using legacy module functions
	env | grep -q LMOD || module purge
	
	unset LOADEDMODULES
	
	unset MODULEPATH
	
	unset MODULESHOME
	
	#in child shells after this has already been sourced, this env var is lmod's, and if it's set, lmod's setup does nothing
	unset MODULEPATH_ROOT
	
	export MANPATH="$(echo "$MANPATH" | sed 's?/n/sw/odyssey-apps/modules-3.2.6/Modules/man:??')"
	
	source /usr/local/bin/lmod.sh
	
	FASRC_MODULE_FLAVOR=lmod
fi
