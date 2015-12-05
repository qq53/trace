#include <netinet/in.h>
#include "call.h"
#include "handler.cpp"

void init_call(){
	for(int i = 0; i < CALL_NUMS; ++i)
		syscall_trace[i] = &empty;
	
#ifdef BIT32
	syscall_trace[SOCKETCALL] = &bind;
#else
	syscall_trace[BIND] = &bind64;
#endif
	syscall_trace[OPEN] = &open;
}

LOCAL_VAR is_user_data(BITS_TYPE addr){
	if( regs.REG_SP <= addr && regs.REG_BP >= addr )
		return STACK;
	else if( rodata_addr_start <= addr && rodata_addr_end > addr)
		return RODATA;
	else
		return NONE;
}

char *check_str(BITS_TYPE addr){
	switch(is_user_data(addr)){
		case STACK:
			return get_str(addr);
			break;
		case RODATA:
			return get_str(addr, rodata_size);
			break;
		default:
			return NULL;
	}
}

char *get_str(BITS_TYPE addr, int m){
	int max_len = m;
	char *str = (char *)malloc(max_len); 
	char *p = str;
	for(int i = 0; i < max_len/sizeof(BITS_TYPE); ++i){
		*(BITS_TYPE *)p = ptrace(PTRACE_PEEKTEXT, child, addr);
		for(int j = 0; j < sizeof(BITS_TYPE); ++j){
			if( p[i] == '\0' )
				break;
		}
		p += sizeof(BITS_TYPE);
		addr += sizeof(BITS_TYPE);
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
