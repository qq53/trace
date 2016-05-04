SFILE=dlsym
PWD=`pwd`
echo $PWD | egrep -i "dlsym" &&
export LD_PRELOAD="$PWD/$SFILE.32.so":"$PWD/$SFILE.64.so" ||
export LD_PRELOAD="$PWD/dlsym/$SFILE.32.so":"$PWD/dlsym/$SFILE.64.so"
