if [ $# -lt 1 ]; then
	g++ main.cpp -o in
else
	case $1 in
	'clean')
		rm in
		;;
	esac
fi
