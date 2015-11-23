typedef void (*fn)(int);

#ifdef BIT32
	#define CALL_NUMS 354
	#define ARG1	  ebx
	#define ARG2	  ecx
	#define ARG3	  edx
	#define ARG4	  esi
	#define ARG5	  edi
	#define BITS_TYPE uint32_t      
#else 
	#define CALL_NUMS 316
	#define ARG1	  rdi
	#define ARG2	  rsi
	#define ARG3	  rdx
	#define ARG4	  rcx
	#define ARG5	  r8
	#define ARG6	  r9
	#define BITS_TYPE uint64_t      
#endif
fn syscall_trace[CALL_NUMS] = {NULL};

void init_call();
