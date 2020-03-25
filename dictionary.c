// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

#define HASHTABLE_SIZE 65536

// Represents a node in a hash
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;



// Hash table
node *table[HASHTABLE_SIZE];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int len = strlen(word);
    char lword[len + 1];
    for (int i = 0; i < len; i++)
    {
        lword[i] = tolower(word[i]);
    }
    lword[len] = '\0';
    
int bucket = hash(lword);
node *cursor = table[bucket];
while (cursor != NULL)
{
    if (strcmp(cursor->word, lword) !=0 )
    
        cursor = cursor->next;
    
    else 
        return true;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
  unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
        hash = (hash << 2) ^ word[i];
    return hash % HASHTABLE_SIZE;
}


int count = 0;
// Loads dictionary into memory, returning true if successful else false

bool load(const char *dictionary)
//open dictionary file
{
    char buffer[LENGTH+1];
    FILE* dic_ptr = fopen(dictionary, "r");

    if (dic_ptr == NULL)
    {
        fprintf(stderr, "something is wrong");
        return 1;
    }

    while(fscanf(dic_ptr, "%s", buffer) != EOF)
    {
        
count++;
    node *newWord = malloc(sizeof(node));

         if (newWord == NULL)
            {
            return 1;
            }
    strcpy(newWord->word, buffer);

// implement hash function to get the index
int index = hash(buffer);

// if the corresponding index in hashtable is empty, assign it to the temp node

if (table[index] == NULL)
table[index]= newWord;

//else if index is occupied, add note to index by adjusting pointers , NewWord to the start of linked list
else
{
    newWord->next = table[index];
    table[index] = newWord;
}

    }
    fclose(dic_ptr);
return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
   return count;
   printf("%i",count);
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    
    
    for (int i = 0; i < 65536; i++)
    {
       node *cursor = table[i];
            while (cursor != NULL)
            
        {
            
           node *tem = cursor->next;
           free(cursor);
           cursor = tem;
           
        }
            
    }
   
    return true;
   

}
