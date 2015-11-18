typedef void(*fn)(int);
fn syscall_trace[354] = {NULL};

void init_call();
int fd;
