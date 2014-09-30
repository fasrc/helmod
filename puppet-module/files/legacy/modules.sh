#----------------------------------------------------------------------#
# system-wide profile.modules                                          #
# Initialize modules for all sh-derivative shells                      #
#----------------------------------------------------------------------#
trap "" 1 2 3

case "$0" in
    -bash|bash|*/bash) . /n/sw/odyssey-apps/modules-3.2.6/Modules/init/bash ;;
       -zsh|zsh|*/zsh) . /n/sw/odyssey-apps/modules-3.2.6/Modules/init/zsh ;;
       -ksh|ksh|*/ksh) . /n/sw/odyssey-apps/modules-3.2.6/Modules/init/ksh ;; 
          -sh|sh|*/sh) . /n/sw/odyssey-apps/modules-3.2.6/Modules/init/sh ;; 
                    *) . /n/sw/odyssey-apps/modules-3.2.6/Modules/init/sh ;; 	# default for scripts
esac

trap 1 2 3

#RC custom
newdir="/n/sw/odyssey-apps/modules-3.2.6/Modules/man"
if ! echo $MANPATH | /bin/egrep -q "(^|:)$newdir($|:)" ; then
	export MANPATH="$newdir:$MANPATH"
fi
export -f module >/dev/null  #so that it's available to scripts
