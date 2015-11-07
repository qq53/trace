/// \file call.cpp
/*
  ------------------------------------
  Create date : 2015-11-07 23:25
  Modified date: 2015-11-07 23:25
  Author : Sen1993
  Email : gsen1993@gmail.com
  ------------------------------------
*/

#include "call.h"

void empty(int n){
	printf("%d: %x\n", n, eax);
}

void call_open(int n){
	printf("open = %x\n", eax);
}

void init_call(){
	//initilize
	for(int i = 0; i < sizeof(syscall_trace)/sizeof(syscall_trace[0]); ++i)
		syscall_trace[i] = &empty;
	
	//special call
	syscall_trace[OPEN] = &call_open;
}

char *checkStr(uint64_t addr, int m = 1000){
	int max_len = m;
	char *str = (char *)malloc(max_len); 
	char *p = str;
	for(int i = 0; i < max_len/sizeof(uint64_t); ++i){
		*(uint64_t *)p = ptrace(PTRACE_PEEKTEXT, child, addr);
		for(int j = 0; j < sizeof(uint64_t); ++j){
			if( p[i] == '\0' )
				break;
		}
		p += sizeof(uint64_t);
		addr += sizeof(uint64_t);
	}
	bool valid = true;
	bool null_end = false;
	int len = 0;
	for(int i = 0; i < max_len; ++i){
		if(str[i] == '\0'){
			null_end = true;
			break;
		}else if(str[i] < 0x20 || str[i] > 0x7e){
			valid = false;
			break;
		}
		++len;
	}
	if(!valid || !null_end || len == 0)
		return NULL;
	return str;
}
