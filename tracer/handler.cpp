#include <linux/net.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include "handler.h"

void empty(int n){}

void def(int n){
	char *p = check_str(GET_ARGS(1));
	if(p)
		printf("%s %s = %x\n", syscall_name[n], p, reg0);
	else
		printf("%s %x = %x\n", syscall_name[n], GET_ARGS(1), reg0);
}

void bind64(int n){
	BITS_TYPE p,port,addr;
	p = GET_ARGS(2);
	port = ntohs(ptrace(PTRACE_PEEKTEXT, child, p)>>16);
	addr = ntohl(ptrace(PTRACE_PEEKTEXT, child, p+4));
	printf("#bind port:%d addr:%d.%d.%d.%d\n",port,
		addr&0xff000000,addr&0xff0000,addr&0xff00,addr&0xff);
}

void socketcall(int n){
	BITS_TYPE p,port,addr;

	switch(GET_ARGS(1)){
		case SYS_BIND:
			p = ptrace(PTRACE_PEEKTEXT, child, GET_ARGS(2)+4);
			port = ntohs(ptrace(PTRACE_PEEKTEXT, child, p)>>16);
			addr = ntohl(ptrace(PTRACE_PEEKTEXT, child, p+4));
			printf("#bind port:%d addr:%d.%d.%d.%d\n",port,
				addr&0xff000000,addr&0xff0000,addr&0xff00,addr&0xff);
			break;
		default:
			p = ptrace(PTRACE_PEEKTEXT, child, GET_ARGS(2));
			printf("%s %x = %x\n", socketcall_name[GET_ARGS(1)], p, reg0);
			break;
	}
}

void open(int n){
	struct stat sbuf;
	const char *file = check_str(GET_ARGS(1));
	stat(file, &sbuf);
	if(sbuf.st_uid == 0)
		printf("#");
	if(file)
		printf("open %s = %x\n", file, reg0);
	else
		printf("open %x = %x\n", GET_ARGS(1), reg0);
}
