#include <stdio.h>
#include "cs50.h"
#include <stdint.h>
#include <string.h>
#include <stdlib.h>


int main(void){
    int money = 0;
    while(money<=0){
        money = get_int("Change owned: ");
    }
    int count=0;
    int rest=money;
    int temp;
    while(rest>0){
        if(rest>=25){
            rest = rest%25;
            temp = money-rest;
            count += temp/25;
            money = rest;
        }
        else if(rest<25 && rest>=10){
            rest = rest%10;
            temp = money-rest;
            count += temp/10;
            money = rest;
        }
        else if(rest<10 && rest>=5){
            rest = rest%5;
            temp = money-rest;
            count += temp/5;
            money = rest;
        }
        else if(rest<5 && rest>=1){
            count += rest;
            rest = 0;
        }
        else continue;
    }
    printf("%d\n", count);
    return 0;
}
