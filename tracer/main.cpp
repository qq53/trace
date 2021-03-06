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
#include <signal.h>

#include "pre.h"
#include "main.h"
#include "call.cpp"

#define STACK_SIZE 0x8000

bool sub_killed = false;

void handler(int a){
	sub_killed = true;
	kill(child, SIGKILL);
}

int main(int argc, char *argv[])
{
    long call_num;
    int status;
    int insyscall = 0;
	int count = 0;
	char **args;
	int fout,fin;

	if(argc < 4){
		printf("Usage: tracer rodata_addr rodata_size xx ...\n");
		return 0;
	}

	rodata_addr_start = atoi(argv[1]);
	rodata_size = atoi(argv[2]);
	rodata_addr_end = rodata_size + rodata_addr_start;

	init_call();

    child = fork();
    if (child == 0) {
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		if(argc <= 4)
			args = NULL;
		else
			args = &argv[4];

		fin = open("subin",O_CREAT | O_RDWR,0666);
		dup2(fin,0);
		close(fin);
		execve(argv[3], args, NULL);
    } else {
		signal(SIGALRM,handler);
		fout = open("out",O_CREAT | O_RDWR | O_TRUNC,0666);
		dup2(fout,1);
		close(fout);
		setbuf(stdout, NULL);
		while (1) {
			wait(&status);
			if(sub_killed)
				break;
			if (WIFEXITED(status))
				break;
			call_num = ptrace(PTRACE_PEEKUSER, child, BYTES * ORIG_REG0, NULL);
			if (insyscall == 0) {
				insyscall = 1;
				if (++count < SKIP_CALLS_NUM)
					goto _skip_call;
				reg0 = ptrace(PTRACE_PEEKUSER, child, BYTES * REG0, NULL);
			} else {
				insyscall = 0;
				if (count <= SKIP_CALLS_NUM)
					goto _skip_call;
				ptrace(PTRACE_GETREGS, child, NULL, &regs);
				syscall_trace[call_num](call_num);
			}
_skip_call:
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);
		}
    }
    return 0;
}
