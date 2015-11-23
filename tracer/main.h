#ifdef BIT32
	#include "call_name_32.h"
	#include "call_num_32.h"
	#define SKIP_CALLS_NUM 21
	#define BYTES 4
	#define ORIG_REG0 ORIG_EAX
	#define REG0 EAX
#else
	#include "call_name_64.h"
	#include "call_num_64.h"
	#define SKIP_CALLS_NUM 24
	#define BYTES 8
	#define ORIG_REG0 ORIG_RAX
	#define REG0 RAX
#endif

pid_t child;
struct user_regs_struct regs;
int reg0;
