// never remove statistics from this structure, they could be
// used by existing exercices. You might add some additional information
// if it can help to validate some exercices
#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

struct params_pthread_create_t {
  pthread_t* restrict thread;
  const pthread_attr_t* restrict attr;
  void* start_routine;
  void* restrict arg;
};

struct stats_pthread_create_t {
  int called;           // number of times the system call has been called
  int last_return;    // last return value 
  struct params_pthread_create_t last_params; // last parameters passed as arguments
};

struct params_pthread_join_t {
  pthread_t thread;
  void** value_ptr;
};

struct stats_pthread_join_t {
  int called;           // number of times the system call has been called
  int last_return;    // last return value 
  struct params_pthread_join_t last_params; // last parameters passed as arguments
};