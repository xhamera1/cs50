#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool is_unique(string k){
    bool char_set[26]={false};
    for (int i = 0; i < strlen(k); ++i) {
        if (k[i] >= 'A' && k[i] <= 'Z') {
            int val = k[i] - 'A';
            if (char_set[val]) {
                return false;
            }
            char_set[val] = true;
        } else if (k[i] >= 'a' && k[i] <= 'z') {
            int val = k[i] - 'a';
            if (char_set[val]) {
                return false;
            }
            char_set[val] = true;
        }
    }
    return true;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("wronlgy passed command with key\n");
        return 1;
    }
    string key = argv[1];
    if(strlen(key)!=26){
        printf("wrongly passed key\n");
            return 1;
    }
    for(int i=0;i<strlen(key);++i){
        if(!isalpha(key[i])){
            printf("wrongly passed key\n");
            return 1;
        }
    }
    if (!is_unique(key)) {
        printf("wrongly passed key\n");
        return 1;
    }
    for (int i = 0; i < strlen(key); ++i) {
        key[i] = toupper(key[i]);
    }
    char normal_letters[26] = {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
    string plaintext = get_string("plaintext: ");
    for(int i=0;i<strlen(plaintext);++i){
        if(isupper(plaintext[i])){
            for(int j=0;j<26;++j){
                if(normal_letters[j]==plaintext[i]){
                    plaintext[i] = key[j];
                    break;
                }
            }
        }
        else{
            char this_but_upper = toupper(plaintext[i]);
            for(int j=0;j<26;++j){
                if(normal_letters[j]==this_but_upper){
                    plaintext[i] = tolower(key[j]);
                    break;
                }
            }
        }
    }
    printf("ciphertext: %s\n",plaintext);

    return 0;
}
