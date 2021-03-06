#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/reg.h>
#include <sys/syscall.h>
#include <sys/user.h>
#include <string.h>
#include <fcntl.h>

#include "pre.h"
#include "main.h"
#include "basecall.cpp"

#define STACK_SIZE 0x8000

int main(int argc, char *argv[])
{
    long call_num;
    int status;
    int insyscall = 0;
	char **args;

	if(argc < 4){
		printf("Usage: tracer xx rodata_addr rodata_size\n");
		return 0;
	}

	rodata_addr_start = atoi(argv[2]);
	rodata_size = atoi(argv[3]);
	rodata_addr_end = rodata_size + rodata_addr_start;

	init_call();

    child = fork();
    if (child == 0) {
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		if(argc <= 4)
			args = NULL;
		else
			args = &argv[4];
		close(1);
		execve(argv[1], args, NULL);
    } else {
		while (1) {
			wait(&status);
			if (WIFEXITED(status))
				break;
			call_num = ptrace(PTRACE_PEEKUSER, child, BYTES * ORIG_REG0, NULL);
			if (insyscall == 0) {
				insyscall = 1;
				reg0 = ptrace(PTRACE_PEEKUSER, child, BYTES * REG0, NULL);
			} else {
				insyscall = 0;
				ptrace(PTRACE_GETREGS, child, NULL, &regs);
				syscall_trace[call_num](call_num);
			}
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);
		}
    }
    return 0;
}
