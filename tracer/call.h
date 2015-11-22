typedef void (*fn)(int);

#ifdef BIT32
	#define CALL_NUMS 354
#else 
	#define CALL_NUMS 316
#endif
fn syscall_trace[CALL_NUMS] = {NULL};

void init_call();
