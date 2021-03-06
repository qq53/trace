PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

function base_make(){
	echo '#define BIT32' > pre.h
	g++ basemain.cpp -o basetracer32 -m32
	echo '' > pre.h
	g++ basemain.cpp -o basetracer64
}

function make_32(){
	echo '#define BIT32' > pre.h
	n=`./basetracer32 base32 0 0 | wc -l`
	echo "#define SKIP_CALLS_NUM $n" >> pre.h
	g++ main.cpp -o tracer32 -m32
}

function make_64(){
	n=`./basetracer64 base64 0 0 | wc -l`
	echo "#define SKIP_CALLS_NUM $n" > pre.h
	g++ main.cpp -o tracer64
}

function clean(){
	rm tracer32
	rm tracer64
	rm basetracer32
	rm basetracer64
}

if [ "$#" -eq 0 ]; then
	base_make
	make_32
	make_64
	exit 0
fi

case $1 in
'32')
	base_make
	make_32
	;;
'64')
	base_make
	make_64
	;;
'base')
	base_make
	;;
'clean')
	clean
	;;
*)
	echo 'param error'
	;;
esac
