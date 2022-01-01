// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of "buckets" in hash table
// Uses one bucket for each alphabet, i.e., a = 0, b = 1, ... , z = 25
const unsigned int N = 26;

// Hash table (array of linked list)
node *table[N];

unsigned int numberOfWords = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *header = table[hash(word)];
    while (header != NULL)
    {
        if (strcasecmp(header->word, word) == 0)
        {
            return true;
        }
        header = header->next;
    }
    return false;
}

// Hash function: hashes word to a number (hashcode/index), corresponding to which "bucket" to store the word in
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 97;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (!dict)
    {
        return false;
    }

    char *wordInDictionary = malloc(LENGTH + 1);
    if (!wordInDictionary)
    {
        return false;
    }

    while (fscanf(dict, "%s", wordInDictionary) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (!n)
        {
            return false;
        }

        strcpy(n->word, wordInDictionary);

        // Inserts node n at the beginning of linked list
        n->next = table[hash(wordInDictionary)];

        // Set node n as the header node for the corresponding "bucket" in hash table
        table[hash(wordInDictionary)] = n;

        numberOfWords++;

        //free(n);   // This is implemented in the unload function
    }

    free(wordInDictionary);
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return numberOfWords;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *header;
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        header = table[i];

        while (header != NULL)
        {
            tmp = header->next;
            free(header);
            header = tmp;
        }
    }

    if (header == NULL)
    {
        return true;
    }
    else
    {
        return false;
    }
}
