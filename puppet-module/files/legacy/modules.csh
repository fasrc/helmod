#----------------------------------------------------------------------#
# system-wide csh.modules                                              #
# Initialize modules for all csh-derivative shells                     #
#----------------------------------------------------------------------#
if ($?tcsh) then
	set modules_shell="tcsh"
else
	set modules_shell="csh"
endif

source /n/sw/odyssey-apps/modules-3.2.6/Modules/init/${modules_shell}

unset modules_shell

#RC custom
if ! ($?MANPATH) then
	setenv MANPATH ""
endif
set newdir = "/n/sw/odyssey-apps/modules-3.2.6/Modules/man"
if ( "${MANPATH}" !~ *":${newdir}:"* && "${MANPATH}" !~ "${newdir}:"* && "${MANPATH}" !~ *":${newdir}" &&  "${MANPATH}" !~ "${newdir}" ) then
	setenv MANPATH "${newdir}:${MANPATH}"
endif
