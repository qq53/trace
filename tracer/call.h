typedef void (*fn)(int);

#ifdef BIT32
	#define CALL_NUMS 354
	#define ARG1	  ebx
	#define ARG2	  ecx
	#define ARG3	  edx
	#define ARG4	  esi
	#define ARG5	  edi
	#define BITS_TYPE uint32_t
	#define REG_SP	  esp
	#define REG_BP	  ebp
#else 
	#define CALL_NUMS 316
	#define ARG1	  rdi
	#define ARG2	  rsi
	#define ARG3	  rdx
	#define ARG4	  rcx
	#define ARG5	  r8
	#define ARG6	  r9
	#define BITS_TYPE uint64_t      
	#define REG_SP	  rsp
	#define REG_BP	  rbp
#endif
fn syscall_trace[CALL_NUMS] = {NULL};

void init_call();
long rodata_addr_start, rodata_addr_end, rodata_size;
char *check_str(BITS_TYPE addr);
char *get_str(BITS_TYPE addr,int size = 100);
