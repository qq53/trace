#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main(int argc, char *argv[]){
	if ( argc <= 1 ){
		puts("Usage: ./in ...");
		return 0;
	}

	int len = 2;
	for(int i = 1; i < argc; ++i)
		len += strlen(argv[i])+1;
	char *cmd = (char *)malloc(len);
	memset(cmd, 0, len);

	strcat(cmd, "./");
	for(int i = 1; i < argc; ++i){
		strcat(cmd, argv[i]);
		strcat(cmd, " ");
	}

	int fin;

	fin = open("subin",O_CREAT | O_RDWR,0666);
	dup2(fin,0);
	close(fin);

	system(cmd);

	return 0;
}
