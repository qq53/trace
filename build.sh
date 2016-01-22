if [ $# -lt 1 ]; then
	echo 'Usage: build.sh [app|out|clean]'
fi

case $1 in
'app')
	cd tracer
	./make.sh
	;;
'out')
	cd dlsym
	./dlsym.sh test32
	cd ../redirect_in
	./make.sh
	;;
'clean')
	cd dlsym
	./dlsym.sh clean
	cd ../redirect_in
	./make.sh clean
	cd ../tracer
	./make.sh clean
	;;
esac
