#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(void) {
    char tab[26][2][10] ={
        {"A", "1"}, {"B", "3"}, {"C", "3"}, {"D", "2"}, {"E", "1"}, {"F", "4"},
        {"G", "2"}, {"H", "4"}, {"I", "1"}, {"J", "8"}, {"K", "5"}, {"L", "1"},
        {"M", "3"}, {"N", "1"}, {"O", "1"}, {"P", "3"}, {"Q", "10"}, {"R", "1"},
        {"S", "1"}, {"T", "1"}, {"U", "1"}, {"V", "4"}, {"W", "4"}, {"X", "8"},
        {"Y", "4"}, {"Z", "10"}
    };

    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    for (int i = 0; i < strlen(word1); ++i) {
        word1[i] = toupper(word1[i]);
    }
    for (int i = 0; i < strlen(word2); ++i) {
        word2[i] = toupper(word2[i]);
    }

    int count1 = 0;
    int count2 = 0;

    for (int i = 0; i < strlen(word1); ++i) {
        char current = word1[i];
        for (int j = 0; j < 26; ++j) {
            if (tab[j][0][0] == current) {
                int x = atoi(tab[j][1]);
                count1 += x;
                break;
            }
        }
    }

    for (int i = 0; i < strlen(word2); ++i) {
        char current = word2[i];
        for (int j = 0; j < 26; ++j) {
            if (tab[j][0][0] == current) {
                int x = atoi(tab[j][1]);
                count2 += x;
                break;
            }
        }
    }

    if (count1 == count2) {
        printf("Tie!\n");
    } else if (count1 < count2) {
        printf("Player 2 wins!\n");
    } else {
        printf("Player 1 wins!\n");
    }
    return 0;
}
