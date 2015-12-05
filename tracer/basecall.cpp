#include "call.h"

void def(int n){
	printf("%s %x = %x\n", syscall_name[n], GET_ARGS(1), reg0);
}

void init_call(){
	for(int i = 0; i < CALL_NUMS; ++i)
		syscall_trace[i] = &def;
}
