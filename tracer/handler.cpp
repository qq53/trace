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

void bind_64(int n){
	BITS_TYPE p,port,addr;
	p = GET_ARGS(2);
	port = ntohs(ptrace(PTRACE_PEEKTEXT, child, p)>>16);
	addr = ntohl(ptrace(PTRACE_PEEKTEXT, child, p+4));
	printf("#bind port:%d addr:%d.%d.%d.%d\n",port,
		addr&0xff000000,addr&0xff0000,addr&0xff00,addr&0xff);
}

void socketcall_32(int n){
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

void open_32_64(int n){
	int arg1 = GET_ARGS(1);
	const char *file = NULL;
	switch(arg1){
		case 0:
			file = "STDIN";
			break;
		case 1:
			file = "STDOUT";
			break;
		case 2:
			file = "STDERR";
			break;
		default:
			file = check_str(arg1);
			break;
	}
	if( arg1 > 2 && file ){
		struct stat sbuf;
		stat(file, &sbuf);
		if(sbuf.st_uid == 0 || strstr(file, "/etc"))
			printf("#");
	}
	printf("open %s = %x\n", file, reg0);
}

const char *get_fd_path(int fd){
	if( fd < 0 )
		return NULL;

	const char *result;
	char *buf = NULL;

	switch(fd){
		case 0:
			result = "STDIN";
			break;
		case 1:
			result = "STDOUT";
			break;
		case 2:
			result = "STDOUT";
			break;
		default:
			char *path = new char[1024];
			buf = new char[1024];
			snprintf(buf, sizeof(buf), "/proc/self/fd/%d", fd);
			if( readlink(buf, path, sizeof(path)-1) != -1 )
				result = path;
			break;
	}

	if( buf )
		delete buf;
	return result;
}

void write_32_64(int n){
	int fd = GET_ARGS(1);
	const char *path = get_fd_path(fd);

	printf("write %s = %x\n", path, reg0);
	
	if( fd > 2 && path )
		delete path;
}
