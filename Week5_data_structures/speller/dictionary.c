// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26*26;

int words_count=0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hash_value = hash(word);
    node *current_node = table[hash_value];
    while(current_node){
        if(strcasecmp(word,current_node->word)==0){
            return true;
        }
        current_node = current_node->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int index = 0;
    for (int i = 0; i < 2 && word[i] != '\0'; i++)
    {
        index = index * 26 + (toupper(word[i]) - 'A');
    }
    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Error while opening dictionary\n");
        return false;
    }
    char word[LENGTH + 1];
    while(fscanf(dict,"%s",word)!=EOF){
        node *new_node = malloc(sizeof(node));
        if(new_node==NULL){
            fclose(dict);
            return false;
        }
        strcpy(new_node->word,word);
        int index = hash(word);
        new_node->next = table[index];
        table[index] = new_node;
        ++words_count;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for(int i=0;i<N;++i){
        node *current_node = table[i];
        while(current_node!=NULL){
            node *next_node = current_node->next;
            free(current_node);
            current_node = next_node;
        }
        table[i] = NULL;
    }
    return true;
}
