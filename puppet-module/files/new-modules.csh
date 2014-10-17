if ! ($?FASRC_MODULE_FLAVOR) then
	setenv FASRC_MODULE_FLAVOR ''
endif
if ($FASRC_MODULE_FLAVOR != 'lmod') then
	module purge
	unset LOADEDMODULES
	unset MODULEPATH
	unset MODULESHOME
	setenv MANPATH `echo "$MANPATH" | sed 's?/n/sw/odyssey-apps/modules-3.2.6/Modules/man:??'`
	source /usr/local/bin/lmod.csh
	setenv FASRC_MODULE_FLAVOR lmod
endif
