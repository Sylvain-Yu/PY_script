#include <stdio.h>

typedef unsigned long uint32;
typedef signed long sint32;
typedef signed long long sint64;



#define MAX_UNSIGNEDVAL(w)     ((uint32)((1ULL<<(w))-1UL))
#define MAX_SIGNEDVAL(w)       ((sint32)((1LL<<(w-1))-1UL))
#define MIN_SIGNEDVAL(w)       ((sint32)((-1LL<<(w-1))))

#define power2(Qf)             ( ((Qf)>0) ? (double)(1.0*(1LL<<(Qf))) :  (double)(1.0/(1LL<<(-(Qf)))) )

#define round_half(d,Qf)       ( ((sint64)((d)*power2((Qf)+1) ) &1)==0 )

#define round_NEG_data(d,Qf)   ( round_half(d,Qf) ? ((sint32)((d)*power2(Qf)))  : (sint32)(((d)*power2(Qf))-1) )
#define round_POS_data(d,Qf)   ( round_half(d,Qf) ? ((sint32)((d)*power2(Qf)))  : (sint32)(((d)*power2(Qf))+1) )
#define round_POS_udata(d,Qf)  ( round_half(d,Qf) ? ((uint32)((d)*power2(Qf)))  : (uint32)(((d)*power2(Qf))+1) )

#define  fixdt_POS(d,w,Qf)     ( (((d)*power2(Qf)) <  MAX_UNSIGNEDVAL(w)) ?  round_POS_udata(d,Qf) : MAX_UNSIGNEDVAL(w) )
#define sfixdt_POS(d,w,Qf)     ( (((d)*power2(Qf)) <  MAX_SIGNEDVAL  (w)) ?  round_POS_data(d,Qf)  : MAX_SIGNEDVAL(w)   )
#define sfixdt_NEG(d,w,Qf)     ( (((d)*power2(Qf)) >  MIN_SIGNEDVAL  (w)) ?  round_NEG_data(d,Qf)  : MIN_SIGNEDVAL(w)   )

#define sfixdt(data,width,Qf) (((data)<0) ? sfixdt_NEG(data,width,Qf) : sfixdt_POS(data,width,Qf))
#define  fixdt(data,width,Qf) (((data)<0) ? 0                         :  fixdt_POS(data,width,Qf)


/**  decode */






void main()
{
uint32 abc = sfixdt(-20,32,16);
printf("abc = 0x%x", abc);


float a = 0;
a = (~abc +1)/ power2(16);
a = (-1) * a;

printf("a = %f", a);

}