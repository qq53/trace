PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

if [ "$#" -eq 0 ]; then
	echo '#define BIT32' > pre.h
	g++ main.cpp -o tracer32 -m32
	echo '' > pre.h
	g++ main.cpp -o tracer64
	exit 0
fi

if [ $1 == '32' ]; then
	echo '#define BIT32' > pre.h
	g++ main.cpp -o tracer32 -m32
elif [ $1 == '64' ]; then
	echo '' > pre.h
	g++ main.cpp -o tracer64
else
	'param not 32 or 64'
fi
