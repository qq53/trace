MYCC=gcc
SFILE=dlsym
MYFILE=_temp

if [ $# -ne 1 ]; then
	echo 'need target_comm'
	exit 1
fi

case $1 in
'clean')
	rm $SFILE.32.so
	rm $SFILE.64.so
	;;
*)
	cp $SFILE.c $MYFILE.c
	sed -i "s/TARGET_COMM/$1/g" $MYFILE.c

	$MYCC -m32 -fPIC -c $MYFILE.c -o $MYFILE.32.o
	$MYCC -fPIC -c $MYFILE.c -o $MYFILE.64.o

	if [ -f $MYFILE.32.o ]; then
		$MYCC -m32 -shared -fPIC -ldl -o $SFILE.32.so $MYFILE.32.o
		$MYCC -shared -fPIC -ldl -o $SFILE.64.so $MYFILE.64.o
	fi

	if [ -f $MYFILE.32.o ]; then
		rm $MYFILE.32.o
		rm $MYFILE.64.o
		rm $MYFILE.c
	fi

	export LD_PRELOAD=`pwd`"/$SFILE.32.so:"`pwd`"/$SFILE.64.so"
esac
