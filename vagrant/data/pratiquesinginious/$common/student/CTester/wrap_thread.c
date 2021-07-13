#include <stdio.h>
#include <stdlib.h>

#include  "wrap.h"

#include <libintl.h> 
#include <locale.h> 
#define _(STRING) gettext(STRING)


int __real_pthread_create(pthread_t *restrict thread, const pthread_attr_t *restrict attr, void *(*start_routine)(void*), void *restrict arg);
int __real_pthread_join(pthread_t thread, void **value_ptr);


extern bool wrap_monitoring;
extern struct wrap_stats_t stats;
extern struct wrap_monitor_t monitored;
extern struct wrap_fail_t failures;
extern struct wrap_log_t logs;

int __wrap_pthread_create(pthread_t *restrict thread, const pthread_attr_t *restrict attr, void *(*start_routine)(void*), void *restrict arg) {

  if(!wrap_monitoring || !monitored.pthread_create) {
    return __real_pthread_create(thread, attr, start_routine, arg);
  }

  stats.pthread_create.called++;
  stats.pthread_create.last_params.thread=thread;
  stats.pthread_create.last_params.attr=attr;
  stats.pthread_create.last_params.start_routine=start_routine;
  stats.pthread_create.last_params.arg=arg;

  if(FAIL(failures.pthread_create)) {
    failures.pthread_create=NEXT(failures.pthread_create);
    stats.pthread_create.last_return=failures.pthread_create_ret;
    return failures.pthread_create_ret;
  }

  int ret = __real_pthread_create(thread, attr, start_routine, arg);
  failures.pthread_create=NEXT(failures.pthread_create);
  stats.pthread_create.last_return = ret;

  return ret;
}

int __wrap_pthread_join(pthread_t thread, void **value_ptr) {

  if(!wrap_monitoring || !monitored.pthread_join) {
    return __real_pthread_join(thread, value_ptr);
  }

  stats.pthread_join.called++;
  stats.pthread_join.last_params.thread=thread;
  stats.pthread_join.last_params.value_ptr=value_ptr;

  if(FAIL(failures.pthread_join)) {
    failures.pthread_join=NEXT(failures.pthread_join);
    stats.pthread_join.last_return=failures.pthread_join_ret;
    return failures.pthread_join_ret;
  }

  int ret = __real_pthread_join(thread, value_ptr);
  failures.pthread_join=NEXT(failures.pthread_join);
  stats.pthread_join.last_return = ret;

  return ret;
}