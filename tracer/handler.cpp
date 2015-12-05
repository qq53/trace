void empty(int n){}

void def(int n){
	printf("%s %x = %x\n", syscall_name[n], GET_ARGS(1), reg0);
}

void bind64(int n){
	BITS_TYPE p,port,addr;
	if(GET_ARGS(1) != 2)
		return;
	p = GET_ARGS(2);
	port = ntohs(ptrace(PTRACE_PEEKTEXT, child, p)>>16);
	addr = ntohl(ptrace(PTRACE_PEEKTEXT, child, p+4));
	printf("bind port:%d addr:%d.%d.%d.%d\n",port,
		addr&0xff000000,addr&0xff0000,addr&0xff00,addr&0xff);
}

void bind(int n){
	BITS_TYPE p,port,addr;
	if(GET_ARGS(1) != 2)
		return;
	p = ptrace(PTRACE_PEEKTEXT, child, GET_ARGS(2)+4);
	port = ntohs(ptrace(PTRACE_PEEKTEXT, child, p)>>16);
	addr = ntohl(ptrace(PTRACE_PEEKTEXT, child, p+4));
	printf("bind port:%d addr:%d.%d.%d.%d\n",port,
		addr&0xff000000,addr&0xff0000,addr&0xff00,addr&0xff);
}

void open(int n){
	printf("open %s\n", check_str(GET_ARGS(1)));
}
