#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>

int main(void){
    string all_text = get_string("Text: ");
    int length = strlen(all_text);
    int sentence_count = 0;
    int letter_count = 0;
    int word_count = 1;
    for(int i=0;i<length;++i){
        if(all_text[i] == '.' ||all_text[i] == '!' || all_text[i] == '?'){
            sentence_count++;
        }
        if(isalpha(all_text[i])){
            letter_count++;
        }
        if(all_text[i]== ' '){
            word_count++;
        }
    }
    double L = ((double) letter_count/word_count)*100;
    double S = ((double) sentence_count/word_count)*100;

    double grade = 0.0588 * L - 0.296 * S - 15.8;
    double result = round(grade);
    int result1 = (int)result;
    if(result1<1){
        printf("Before Grade 1\n");
    }
    else if(result1>=16){
        printf("Grade 16+\n");
    }
    else{
        printf("Grade %d\n",result1);
    }
    return 0;
}
