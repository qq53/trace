#include <stdio.h>
#include <fcntl.h>

int main(){
	int a,b;
	printf("Hello world\n");
	//a = open("tmp",O_RDWR | O_CREAT);
	a = open("tmp",O_RDWR);
	b = write(a, "1234567890", 10);
	printf("%d,%d\n",a,b);
	return 0;
}
