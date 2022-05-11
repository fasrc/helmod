#/usr/bin/env

# Copyright (c) 2013, John A. Brunelle
# All rights reserved

helpstr="\
NAME
    generate_setup.sh/setup.sh - handle shell environment setup things

SYNOPSIS
    generate_setup.sh/setup.sh [OPTIONS] [DIRECTORY]

DESCRIPTION
    This script is used for setting up the environment, or for creating code 
    that will setup the environment, for software that's laid out in the 
    Filesystem Hierarchy Standard (GNU) way under a prefix -- i.e. directories 
    named \`bin' should be added to the PATH, directories named \`lib' added to 
    LD_LIBRARY_PATH, etc.  Copy this script as-is for a general purpose 
    setup.sh, or use it with options for printing out a setup.sh file or code 
    to be used in modules files (see http://modules.sourceforge.net/).

    DIRECTORY can be used to specify the directory in which to look.  The 
    default is the parent directory of this script's location.  See EXAMPLES 
    below for details.

    This script is aggressive in setting variables, e.g. it adds any 
    directories named \`include' to both CPATH and FPATH, even though there is 
    often only one of those two languages used.  To avoid clutter, it's 
    suggested to double check what it does.

    In addition to searching for the normal GNU layout, this script also has an 
    option -x/--executables to add to PATH all subdirectories with executables 
    in them.

    This script will not dig into .git, .svn, or CVS directories.

    Note that although setup.sh is a more appropriate name for this script, it 
    is NOT named so -- bash's source built-in searches PATH before looking in 
    PWD for files, and this could really mess up people used to doing \`source 
    setup.sh' and not \`source ./setup.sh'.  Furthermore, if you run 
    \`generate_setup.sh DIRECTORY', it only sets up the environment, it does 
    not write out DIRECTORY/setup.sh, as the name may imply.

OPTIONS
    --format FORMAT
        FORMAT values can be:
         
         * bash
         
         * modules

           environment modules in TCL format, for use with 
           http://modules.sourceforge.net/
         
         * lmod

           environment modules in lua format, for use with
           https://www.tacc.utexas.edu/tacc-projects/lmod
           
        The default is \`bash'.

    --action ACTION
        ACTION values can be \`echo', to just print the code to the screen, or 
        \`eval', to actually evaluate it.  \`eval' only works for \`--format 
        bash'.  Default is \`eval'.
    
    --max-depth LEVELS
        Maximum depth at which to look (find's -maxdepth option).  Default is 
        effectively infinite.

    -x, --executables
        Add to PATH all the subdirectories with executables in them that are 
        found within the directory in which this script lives.  Only 
        directories to --max-depth are added.  By default, this is done in 
        addition to the normal search and therefore may add directories to the 
        PATH twice; see also --no-fhs-search.

    --no-fhs-search
        Do not do the standard search for bin, lib, etc.  Use in combination 
        with -x/--executables, otherwise this script will do nothing.

    -p, --prefix STRING
        Use the given STRING for the prefix in the output, instead of the 
        absolute path of the directory given on the command line.
    
    -m, --modules-format
        Legacy.  Shorthand for \`--format modules --action echo'.

    -h, --help
        Print this help.

EXAMPLES
    As-is, this script functions as a normal setup.sh, and it's dynamic:
        install -m 644 \`which generate_setup.sh\` PATH/TO/SOFTWARE/setup.sh
    
    To generate a cleaner but static version, use the following:
        generate_setup.sh --action echo PATH/TO/SOFTWARE > PATH/TO/SOFTWARE/setup.sh
    
    To print code for a modules file, use:
        generate_setup.sh --format modules --action echo PATH/TO/SOFTWARE

REQUIREMENTS
    If no DIRECTORY is given, this requires the BASH_SOURCE variable, something 
    that was introduced around version 3 of bash.

AUTHOR
	Copyright (c) 2013, John A. Brunelle
	All rights reserved
"

directory=''  #the default is set below (we don't want to use BASH_SOURCE unless we have to)
maxdepth=999999999
format='bash'
action='eval'
executables=false
prefix='54ca5f88e43f4ef993b54ba2d21b24ba'  #a magic string, to allow '' prefix
no_fhs_search=false

#hack to avoid digging into version control directories
prunes="-name .git -o -name .svn -o -name CVS"

args=$(getopt -l format:,action:,max-depth:,executables,no-fhs-search,prefix:,modules-format,help -o xp:mh -- "$@")
if [ $? -ne 0 ]; then
	#(getopt will have written the error message)
	return 65 &>/dev/null  #(this script will often be sourced)
	exit 65
fi
eval set -- "$args"
while [ ! -z "$1" ]; do
	case "$1" in
		--format)
			format="$2"
			shift
			case "$format" in
				bash | modules | lmod)
					;;
				*)
					echo "*** ERROR *** [$format] is not a valid --format" >&2
					return 1 &>/dev/null  #(this script will often be sourced)
					exit 1
					;;
			esac
			;;
		--action)
			action="$2"
			shift
			case "$action" in
				echo | eval)
					;;
				*)
					echo "*** ERROR *** [$action] is not a valid --action" >&2
					return 1 &>/dev/null  #(this script will often be sourced)
					exit 1
					;;
			esac
			;;
		--max-depth)
			maxdepth="$2"
			shift
			;;
		-x | --executables)
			executables=true
			;;
		--no-fhs-search)
			no_fhs_search=true
			;;

		-p | --prefix)
			prefix="$2"
			shift
			;;

		-m | --modules-format)
			format=modules
			action=echo
			;;

		-h | --help)
			echo -n "$helpstr"
			return 0 &>/dev/null  #(this script will often be sourced)
			exit 0
			;;
		--) 
			shift
			break
			;;
	esac
	shift
done

directory="$1"
if [ -z "$directory" ]; then
	if [ -z "$BASH_SOURCE" ]; then
		echo "*** ERROR *** your bash is too old -- there's no BASH_SOURCE in the environment" >&2
		return 1 &>/dev/null  #(this script will often be sourced)
		exit 1
	fi
	directory="$(dirname "$(readlink -e "$BASH_SOURCE")")"
else
	directory="$(readlink -e "$directory")"
fi
test "$prefix" = '54ca5f88e43f4ef993b54ba2d21b24ba' && prefix="$directory"
test -n "$prefix" && prefix="$prefix/"

if [ "$format" = modules ] && [ "$action" = eval ]; then
	echo "*** ERROR *** --action eval only supported with --format bash" >&2
	return 1 &>/dev/null  #(this script will often be sourced)
	exit 1
fi


#---


function doit() {
	d="$1"
	var="$2"
	width=20  #max width of any var, plus two
	
	d=${d##./}
	space="$(printf '%'$(( $width - $(echo "$var" | wc -c )))s ' ')"
	case "$format" in
		bash)
			s='export '$space$var'="'"$prefix$d"':$'$var'"'
			;;
		modules)
			s='prepend-path '$var$space' '"$prefix$d"
			;;
		lmod)
			s='prepend_path("'$var'",'$space'"'$prefix$d'")'
	esac
	$action "$s"
}

if ! $no_fhs_search; then
	for pair in \
		bin/PATH \
		include/CPATH \
		include/FPATH \
		info/INFOPATH \
		lib/LD_LIBRARY_PATH \
		lib/LIBRARY_PATH \
		lib64/LD_LIBRARY_PATH \
		lib64/LIBRARY_PATH \
		man/MANPATH \
		pkgconfig/PKG_CONFIG_PATH \
		sbin/PATH \
		site-packages/PYTHONPATH \
	; do
		read -r dir var <<< $(echo $pair | tr / ' ')
		for d in $(cd "$directory" && find -L . -maxdepth "$maxdepth" \( $prunes \) -prune -o \( -type d -a -name "$dir" \) -print ); do
			doit "$d" "$var"
		done
	done
fi

if $executables; then
	var=PATH
	for d in $(cd "$directory" && find -L . -maxdepth "$(( maxdepth + 1))" \( $prunes \) -prune -o \( -type f -a -perm -u=x \) -print0 | xargs -0 -n 1 dirname | sort | uniq); do
		doit "$d" "$var"
	done
fi
