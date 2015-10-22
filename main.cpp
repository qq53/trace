/// \file main.cpp
/*
  ------------------------------------
  Create date : 2015-10-22 17:24
  Modified date: 2015-10-22 22:07
  Author : Sen1993
  Email : gsen1993@gmail.com
  ------------------------------------
*/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/reg.h>
#include <sys/syscall.h>
#include <sys/user.h>

#include "call.h"

pid_t child;

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

int main(int argc, char *argv[])
{
    long orig_rax, eax;
    long params[3];
    int status;
    int insyscall = 0;
    struct user_regs_struct regs;
	int count = 0;
	bool pass = false;

	if(argc < 2){
		printf("Usage trace xx\n");
		return 0;
	}

    child = fork();
    if (child == 0) {
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		execve(argv[1], NULL, NULL);
    } else {
		while (1) {
			wait(&status);
			if (WIFEXITED(status))
				break;
			orig_rax = ptrace(PTRACE_PEEKUSER, child, 8 * ORIG_RAX, NULL);
			if (insyscall == 0) {
				insyscall = 1;
				ptrace(PTRACE_GETREGS, child, NULL, &regs);
				if(count++ < 25)
					goto _n;
				if(regs.rbp - regs.rsp > 0x8000)
					pass = true;
				if(pass)
					goto _n;
				char *s = checkStr(regs.rdi);
				if(s){
					printf("%s\n", s);
					free(s);
				}
				printf("[%x - %x] %s(%x,%x,%x) = ", regs.rsp, regs.rbp, syscall_name[orig_rax], regs.rdi, regs.rsi, regs.rdx);
			} else {
				insyscall = 0;
				if(pass){
					pass = false;
					goto _n;
				}
				if(count <= 25)
					goto _n;
				eax = ptrace(PTRACE_PEEKUSER, child, 4 * RAX, NULL);
				printf("%x\n", eax);
			}
_n:
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);
		}
    }
    return 0;
}
