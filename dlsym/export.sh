SFILE=dlsym
export LD_PRELOAD=`pwd`"/dlsym/$SFILE.32.so:"`pwd`"/dlsym/$SFILE.64.so"
