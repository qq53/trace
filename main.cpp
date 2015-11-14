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

#include "main.h"
#include "call_name.h"
#include "call_num.h"
#include "call.cpp"

#define STACK_SIZE 0x8000

int main(int argc, char *argv[])
{
    long orig_rax;
    int status;
    int insyscall = 0;
	int count = 0;
	char **args;
	int count_key = 25;

	if(argc < 2){
		printf("Usage trace xx\n");
		return 0;
	}

	init_call();

	count_key += atoi(argv[1]);

    child = fork();
    if (child == 0) {
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		if(argc <= 3)
			args = NULL;
		else
			args = &argv[3];
		execve(argv[2], args, NULL);
    } else {
		while (1) {
			wait(&status);
			if (WIFEXITED(status))
				break;
			orig_rax = ptrace(PTRACE_PEEKUSER, child, 4 * ORIG_EAX, NULL);
			if (insyscall == 0) {
				insyscall = 1;
				ptrace(PTRACE_GETREGS, child, NULL, &regs);
				if(count++ < count_key)
					goto _n;
			} else {
				insyscall = 0;
				if(count <= count_key)
					goto _n;
				syscall_trace[orig_rax](orig_rax);
			}
_n:
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);
		}
    }
    return 0;
}
