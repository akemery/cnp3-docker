#include<stdio.h>
#include<stdlib.h>
#include <limits.h>

int powersol(int p, int n)
{
   int  x = 1;
   if(p == 0)
     return 0;
   if(p > INT_MAX)
     return -1;
   for(x = 1;  n > 0 ; --n){
     if(x > INT_MAX/p)
        return -1;
     x=x*p;
   }
   return(x);
}