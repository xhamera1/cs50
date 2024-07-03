#include <stdio.h>
#include <cs50.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int main(void){
    int n=0;
    while(n<=0){
        n = get_int("Height: ");
    }
    char* piramid = malloc(n*sizeof(char)+1);
    for(int k=0;k<n;++k){
        piramid[k] = ' ';
    }
    piramid[n] = '\0';
    for(int i=n-1;i>=0;--i){
        piramid[i] = '#';
        for(int j=0;j<strlen(piramid);++j){
            printf("%c",piramid[j]);
        }
        printf("\n");

    }
    free(piramid);
    return 0;
}
