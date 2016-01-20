#define _GNU_SOURCE

#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <stdarg.h>
#include <fcntl.h>

const char *target = "TARGET_COMM";

int filter(){
	int fd;
	char *path;
	char buf[10] = {};

	asprintf(&path, "/proc/%d/comm", getpid());
	fd = open(path, O_RDONLY);
	if( fd == -1 )
		return 0;
	
	read(fd, buf, 10);
	close(fd);

	if ( strncmp(target, buf, strlen(target)) == 0 )
		return 1;
	return 0;
}

void my_write(const char *s){
	int fd;

	if ( filter() == 0 )
		return;

	fd = open("subout",O_CREAT | O_RDWR | O_APPEND,0666);
	write(fd, s, strlen(s));
	close(fd);
}

int printf(const char *format, ...){
	va_list list;
	char *parg;
	typeof(printf) *old_printf;

	va_start(list, format);
	vasprintf(&parg, format, list);
	va_end(list);

	my_write(parg);

	old_printf = dlsym(RTLD_NEXT, "printf");
	(*old_printf)("%s", parg);

	free(parg);
}

int puts(const char *s){
	typeof(puts) *old_puts;

	my_write(s);

	old_puts = dlsym(RTLD_NEXT, "puts");
	(*old_puts)(s);
}
