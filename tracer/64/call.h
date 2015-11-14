/// \file call.h
/*
  ------------------------------------
  Create date : 2015-11-07 23:24
  Modified date: 2015-11-07 23:24
  Author : Sen1993
  Email : gsen1993@gmail.com
  ------------------------------------
*/

typedef void (*fn)(int);
fn syscall_trace[316] = {NULL};

void init_call();
