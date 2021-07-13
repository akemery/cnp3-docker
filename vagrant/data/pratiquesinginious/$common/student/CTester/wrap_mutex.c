#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include "wrap.h" // system call wrapper
#include <pthread.h>
#include <libintl.h>

#define _(STRING) gettext(STRING)


//int pthread_mutex_lock(pthread_mutex_t *mutex);
//int pthread_mutex_trylock(pthread_mutex_t *mutex);
//int pthread_mutex_unlock(pthread_mutex_t *mutex); 


int __real_pthread_mutex_lock(pthread_mutex_t *mutex);
int __real_pthread_mutex_trylock(pthread_mutex_t *mutex);
int __real_pthread_mutex_unlock(pthread_mutex_t *mutex); 
int __real_pthread_mutex_init(pthread_mutex_t *restrict mutex, const pthread_mutexattr_t *restrict attr);
int __real_pthread_mutex_destroy(pthread_mutex_t *mutex);

extern bool wrap_monitoring;
extern struct wrap_stats_t stats;
extern struct wrap_monitor_t monitored;
extern struct wrap_fail_t failures;
extern void push_info_msg(char* msg);
extern pthread_mutex_t mut;

int err;

/*void init_mutex() {
  //nothing to do
}

void clean_mutex() {
  //nothing to do
}*/

void resetstats_mutex() {

  stats.pthread_mutex_lock.called=0;
  stats.pthread_mutex_lock.last_return=0;
  stats.pthread_mutex_trylock.called=0;
  stats.pthread_mutex_trylock.last_return=0;
  stats.pthread_mutex_unlock.called=0;
  stats.pthread_mutex_unlock.last_return=0;
  stats.pthread_mutex_init.called=0;
  stats.pthread_mutex_init.last_return=0;
  stats.pthread_mutex_destroy.called=0;
  stats.pthread_mutex_destroy.last_return=0;
}

int __wrap_pthread_mutex_destroy(pthread_mutex_t *mutex) {
  if(!wrap_monitoring || !monitored.pthread_mutex_destroy) {
    return __real_pthread_mutex_destroy(mutex);
  }
  // being monitored

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  stats.pthread_mutex_destroy.called++;
  stats.pthread_mutex_destroy.last_arg=mutex;

  if(FAIL(failures.pthread_mutex_destroy)) {
    failures.pthread_mutex_destroy=NEXT(failures.pthread_mutex_destroy);
    errno = failures.pthread_mutex_destroy_errno;
    stats.pthread_mutex_destroy.last_return=failures.pthread_mutex_destroy_ret;
    return failures.pthread_mutex_destroy_ret;
  }

  int ret=__real_pthread_mutex_destroy(mutex);
  stats.pthread_mutex_destroy.last_return=ret;
  failures.pthread_mutex_destroy=NEXT(failures.pthread_mutex_destroy);

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  return ret;
}


int __wrap_pthread_mutex_init(pthread_mutex_t *restrict mutex,
                       const pthread_mutexattr_t *restrict attr) {
  if(!wrap_monitoring || !monitored.pthread_mutex_init) {
    return __real_pthread_mutex_init(mutex,attr);
  }
  // being monitored

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  stats.pthread_mutex_init.called++;
  stats.pthread_mutex_init.last_arg=mutex;

  if(FAIL(failures.pthread_mutex_init)) {
    failures.pthread_mutex_init=NEXT(failures.pthread_mutex_init);
    errno = failures.pthread_mutex_init_errno;
    stats.pthread_mutex_init.last_return=failures.pthread_mutex_init_ret;
    return failures.pthread_mutex_init_ret;
  }
  
  int ret=__real_pthread_mutex_init(mutex,attr);
  stats.pthread_mutex_init.last_return=ret;
  failures.pthread_mutex_init=NEXT(failures.pthread_mutex_init);

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  return ret;

}


pid_t __wrap_pthread_mutex_lock(pthread_mutex_t *mutex) {
  if(!wrap_monitoring || !monitored.pthread_mutex_lock) {
    return __real_pthread_mutex_lock(mutex);
  }
  // being monitored

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  if(FAIL(failures.pthread_mutex_lock)) {
    failures.pthread_mutex_lock=NEXT(failures.pthread_mutex_lock);
    errno = failures.pthread_mutex_lock_errno;
    stats.pthread_mutex_lock.last_return=failures.pthread_mutex_lock_ret;
    stats.pthread_mutex_lock.called++;
    stats.pthread_mutex_lock.last_arg=mutex;

    err = __real_pthread_mutex_unlock(&mut);
    if(err){
      push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
      return err;
    }

    return failures.pthread_mutex_lock_ret;
  }

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  int ret=__real_pthread_mutex_lock(mutex);

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  failures.pthread_mutex_lock=NEXT(failures.pthread_mutex_lock);
  stats.pthread_mutex_lock.called++;
  stats.pthread_mutex_lock.last_arg=mutex;
  stats.pthread_mutex_lock.last_return=ret;

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  return ret;

}

pid_t __wrap_pthread_mutex_trylock(pthread_mutex_t *mutex) {
  if(!wrap_monitoring || !monitored.pthread_mutex_trylock) {
    return __real_pthread_mutex_trylock(mutex);
  }
  // being monitored

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  if(FAIL(failures.pthread_mutex_trylock)) {
    failures.pthread_mutex_trylock=NEXT(failures.pthread_mutex_trylock);
    errno = failures.pthread_mutex_trylock_errno;
    stats.pthread_mutex_trylock.last_return=failures.pthread_mutex_trylock_ret;
    stats.pthread_mutex_trylock.called++;
    stats.pthread_mutex_trylock.last_arg=mutex;

    err = __real_pthread_mutex_unlock(&mut);
    if(err){
      push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
      return err;
    }

    return failures.pthread_mutex_trylock_ret;
  }

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  int ret=__real_pthread_mutex_trylock(mutex);

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  failures.pthread_mutex_trylock=NEXT(failures.pthread_mutex_trylock);
  stats.pthread_mutex_trylock.called++;
  stats.pthread_mutex_trylock.last_arg=mutex;
  stats.pthread_mutex_trylock.last_return=ret;

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  return ret;

}

pid_t __wrap_pthread_mutex_unlock(pthread_mutex_t *mutex) {
  if(!wrap_monitoring || !monitored.pthread_mutex_unlock) {
    return __real_pthread_mutex_unlock(mutex);
  }
  // being monitored

  err = __real_pthread_mutex_lock(&mut);
  if(err){
    push_info_msg(_("Can't lock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  if(FAIL(failures.pthread_mutex_unlock)) {
    failures.pthread_mutex_unlock=NEXT(failures.pthread_mutex_unlock);
    errno = failures.pthread_mutex_unlock_errno;
    stats.pthread_mutex_unlock.last_return=failures.pthread_mutex_unlock_ret;
    stats.pthread_mutex_unlock.called++;
    stats.pthread_mutex_unlock.last_arg=mutex;

    err = __real_pthread_mutex_unlock(&mut);
    if(err){
      push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
      return err;
    }

    return failures.pthread_mutex_unlock_ret;
  
  }

  stats.pthread_mutex_unlock.called++;
  stats.pthread_mutex_unlock.last_arg=mutex;
  failures.pthread_mutex_unlock=NEXT(failures.pthread_mutex_unlock);

  err = __real_pthread_mutex_unlock(&mut);
  if(err){
    push_info_msg(_("Can't unlock mutex in CTester/wrap_mutex.c, please contact your tutor or an administrator"));
    return err;
  }

  int ret=__real_pthread_mutex_unlock(mutex);
  stats.pthread_mutex_unlock.last_return=ret;

  return ret;
}
