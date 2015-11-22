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

#include "main.h"
#include "pre.h"
#ifdef BIT32
	#include "call_name_32.h"
	#include "call_num_32.h"
#else
	#include "call_name_64.h"
	#include "call_num_64.h"
#endif
#include "call.cpp"

#define STACK_SIZE 0x8000

int main(int argc, char *argv[])
{
    long orig_rax;
    int status;
    int insyscall = 0;
	int count = 0;
	char **args;
#ifdef BIT32
	int count_key = 26;
#else
	int count_key = 27;
#endif

	if(argc < 2){
		printf("Usage trace xx\n");
		return 0;
	}

	init_call();

    child = fork();
    if (child == 0) {
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		if(argc <= 2)
			args = NULL;
		else
			args = &argv[2];
		close(1);
		execve(argv[1], args, NULL);
    } else {
		while (1) {
			wait(&status);
			if (WIFEXITED(status))
				break;
#ifdef BIT32
			orig_rax = ptrace(PTRACE_PEEKUSER, child, 4 * ORIG_EAX, NULL);
#else
			orig_rax = ptrace(PTRACE_PEEKUSER, child, 8 * ORIG_RAX, NULL);
#endif
			if (insyscall == 0) {
				insyscall = 1;
#ifdef BIT32
				eax = ptrace(PTRACE_PEEKUSER, child, 4 * EAX, NULL);
#else
				eax = ptrace(PTRACE_PEEKUSER, child, 8 * RAX, NULL);
#endif	
				if(count++ < count_key)
					goto _n;
			} else {
				insyscall = 0;
				if(count <= count_key)
					goto _n;
				ptrace(PTRACE_GETREGS, child, NULL, &regs);
				syscall_trace[orig_rax](orig_rax);
			}
_n:
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);
		}
    }
    return 0;
}
