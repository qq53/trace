if [ $# -lt 1 ]; then
	echo 'Usage: build.sh [app|out|clean|all]'
fi

case $1 in
'all')
	cd tracer
	./make.sh
	cd ../dlsym
	./dlsym.sh tmp
	cd ../redirect_in
	./make.sh
	;;
'app')
	cd tracer
	./make.sh
	;;
'out')
	cd dlsym
	./dlsym.sh tmp
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
