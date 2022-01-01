#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


// Prototype
string substituteWithKeys(string plaintext, string key);


int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    int len = strlen(key);

    if (len != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < len; ++i)
    {
        unsigned char c = key[i];
        if (!isalpha(c))
        {
            printf("The key must contain only letters.\n");
            return 1;
        }
        if (strchr(key + i + 1, c))
        {
            printf("The key must not contain duplicate letters.\n");
            return 1;
        }
    }

    string plaintext = get_string("plaintext:   ");
    string ciphertext = substituteWithKeys(plaintext, key);
    printf("ciphertext:  %s\n", ciphertext);

    return 0;
}

string substituteWithKeys(string plaintext, string key)
{
    string ciphertext = plaintext;

    for (int i = 0, n = strlen(plaintext); i < n; ++i)
    {
        if (isalpha(plaintext[i]))
        {
            if (islower(plaintext[i]))
            {
                ciphertext[i] = tolower(key[tolower(plaintext[i]) - 97]);
            }
            if (isupper(plaintext[i]))
            {
                ciphertext[i] = toupper(key[toupper(plaintext[i]) - 65]);
            }
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    return ciphertext;
}