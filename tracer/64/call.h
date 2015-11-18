typedef void (*fn)(int);
fn syscall_trace[316] = {NULL};

void init_call();
int fd;
