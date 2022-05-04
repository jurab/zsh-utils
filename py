#!/bin/zsh

GIT_DIR="/Users/jurabrazdil/Git"
ENV_DIR="/Users/jurabrazdil/Venvs"

PYTHON="/usr/local/bin/python3.10"
ATOM="/usr/local/bin/atom"

_remove_env() {
	if [[ ! -d ~/Venvs/$1 ]] ; then
		echo "${RED}Error${NC}: Environment $1 does not exist."
		return -1
	fi

	if [ $1 = "default" ] ; then
		echo "${RED}Error${NC}: Cannot remove default environment."
		return -1
	fi

	rm -rf ~/Venvs/$1
	echo "Environment $1 ${RED}removed${NC}."
}


_create_env() {

	# Environment already exists
	if [ -d "$ENV_DIR"/$1 ] ; then
		echo "${RED}Error${NC}: Environment $1 already exists. Skip (-c) to activate."
		return -1
	fi

	$PYTHON -m venv ~/Venvs/$1
	source "$ENV_DIR"/$1/bin/activate
	echo "Environment $1 ${GREEN}created${NC}."
}


_activate_env() {
	source "$ENV_DIR"/$1/bin/activate
}


_open_atom() {
	$ATOM "$(basename "$VIRTUAL_ENV" | awk '{print "~/Git/"$1}')"
}


py() {
	env_name="default"
	action="default"
	open_atom=false

	while [ ! $# -eq 0 ]
		do
			case "$1" in

				--help | -h)
					echo "No options will activate the passed environment."
					echo "	-a, --atom			Open atom in the Git directory."
					echo "	-c, --create			Create new environment."
					echo "	-h, --help			Show help."
					echo "	-l, --list			List environments."
					echo "	-r, --remove			Remove environment."
					echo ""
					;;

				--create | -c)
					action="create"
					;;

				--remove | -r)
					action="remove"
					;;

				--list | -l)
					ls ~/Venvs/
					return 0
					;;

				--atom | -a)
					open_atom=true
					;;

				*)
					env_name=$1
					;;

			esac
			shift
		done

	case "$action" in
		default)
			_activate_env $env_name
			if [ $open_atom = true ] ; then
				_open_atom
			fi
			cd $GIT_DIR/$env_name
			;;
		create)
			_create_env $env_name
			pip install --upgrade pip
			_activate_env $env_name
			cd ~/Git/$env_name
			;;
		remove)
			deactivate &> /dev/null
			_remove_env $env_name
	esac

}
