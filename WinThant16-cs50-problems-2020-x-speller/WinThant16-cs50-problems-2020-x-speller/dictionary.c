// Implements a dictionary's functionality

#include "dictionary.h"

#include <strings.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Number of buckets in hash table
const unsigned int N = 65536;    

// Hash table
node *table[N];

int totalwordcount = 0;



// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    //create variable to traverse
    //the variable is initially a pointer to first element in linked list
    node *cursor = table[hash(word)];

    //compare words
    if (strcasecmp(cursor->word, word) == 0)
    {
        return true;
    }
    //loop until end of list or word found
    while (cursor->next != NULL)
    {
        cursor = cursor->next;
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
//hash function createdd by Daniel J.Bernstein
//adapted djb2 hash from "https://theartincode.stanis.me/008-djb2/#:~:text=The%20simple%20C%20function%20starts,the%20current%20character%20to%20it.")
unsigned int hash(const char *word)
{
    // TODO
    int n = (int) tolower(word[0]) - 97;
    return n;
}




// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO

    //opens dictionary file first
    FILE *file = fopen(dictionary, "r");
    //assigning temp buffer for dictwords
    char *dword_buffer = malloc(LENGTH);
    // checks if dictionary is opened successfully
    if (dword_buffer == NULL)
    {
        return false;
    }

    while (fscanf(file, "%s", dword_buffer) != EOF)
    {
        //allocate memory space for dictionary words
        
        node *n = malloc(sizeof(node)); //makes node for each word in dictionary file

        //check if malloc returns NULL
        if (n == NULL)
        {
            return false;
        }

        //copy each word to different node
        strcpy(n->word, dword_buffer);
        totalwordcount++;

        //setting next pointer to original beginning of list
        n->next = table[hash(dword_buffer)];

        //setting the current new  node as head
        table[hash(dword_buffer)] = n;
    }
    fclose(file);
    free(dword_buffer);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO

    return totalwordcount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    //two variables for iteration
    node *cursor; //looks at first element in list
    node *tmp; //tmp = cursor, free tmp with cursor = cursor->next
    
    
    //recursion for every element in table until NULL
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = cursor;
        
        if (table[i] == NULL)
        {
            continue;
        }
        
    
        while (cursor->next != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
        free(cursor);
    }
    return true;
}
