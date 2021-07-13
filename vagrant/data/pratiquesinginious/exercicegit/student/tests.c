#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <limits.h>
#include "student_code.h"
#include "solutions/student_code_sol.h"
#include "../../course/common/student/CTester/CTester.h"


int get_random(){
   int i = rand()%12;
   while (i<2)
       i= rand()%12;
   return i;
}

void test_power_int() {
	set_test_metadata("puissance", _("test the function puissance"), 1);
    int i1, i2;
    int sol1;
	srand(time(NULL));
	i1 = get_random();
    i2 = get_random();
   
    
	int ret1 = 0;
	int ret2 = 0;
	int ret3 = 0;
    int ret4 = 0;
	int ret5 = 0;
	int ret6 = 0;

	SANDBOX_BEGIN;
	ret1 = power(i1,i2);
	ret2 = power(0,0);
	ret3 = power(0,1);
    ret4 = power(1,0);
    ret5 = power(INT_MAX,1);
    ret6 = power(INT_MAX,2);
	SANDBOX_END;
 
    sol1 = powersol(i1,i2);
   
	CU_ASSERT_EQUAL(ret1, sol1);
	CU_ASSERT_EQUAL(ret2, 0);
	CU_ASSERT_EQUAL(ret3, 0);
    CU_ASSERT_EQUAL(ret4, 1);
	CU_ASSERT_EQUAL(ret5, INT_MAX);
	CU_ASSERT_EQUAL(ret6, -1);

	if (ret1!=sol1){
		char *errtpl = _("power returns the wrong value: you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret1, i1,i2);
		push_info_msg(errmsg);
	}
	if (ret2!=0){
		char *errtpl = _("power returns the wrong value: you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret2, 0,0);
		push_info_msg(errmsg);
	}
	if (ret3!=0){
		char *errtpl = _("power returns the wrong value: you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret3, 0,1);
		push_info_msg(errmsg);
	}
    
    if (ret4!=1){
		char *errtpl = _("power returns the wrong value: you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret4, 1,0);
		push_info_msg(errmsg);
	}
    
    if (ret5!=INT_MAX){
		char *errtpl = _("power returns the wrong value: you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret5, INT_MAX,1);
		push_info_msg(errmsg);
	}
    
    if (ret6!=-1){
		char *errtpl = _("power returns the wrong value should signal overflow with (-1): you returned %d for power(%d,%d)");
		char errmsg[strlen(errtpl+30)];
		sprintf(errmsg, errtpl, ret6, INT_MAX,2);
		push_info_msg(errmsg);
	}
   
	if(sol1==ret1 && ret2==0 && ret3==0 && ret4==1 && ret5==INT_MAX && ret6==-1){
		set_tag("q1");
	}
}
int main(int argc,char** argv)
{
	BAN_FUNCS();
	RUN(test_power_int);
}

