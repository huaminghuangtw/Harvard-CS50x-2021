#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


// Prototype
/* Compute readability level needed to comprehend the text using Coleman–Liau index */
int compute_grade(string text);


int main(void)
{
    string text = get_string("Text:  ");

    int grade = compute_grade(text);
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

    return 0;
}

int compute_grade(string text)
{
    int countOfLetters = 0;
    int countOfWords = 0;
    int countOfSentences = 0;

    for (int i = 0, n = strlen(text); i < n; ++i)
    {
        if (isalpha(text[i]))
        {
            countOfLetters++;
        }

        if (isspace(text[i]))
        {
            countOfWords++;
        }

        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            countOfSentences++;
        }
    }

    // Last word in the last sentence will not be detected. We need to manaully account for it!
    countOfWords++;

    printf("%i letter(s)\n", countOfLetters);
    printf("%i word(s)\n", countOfWords);
    printf("%i sentence(s)\n", countOfSentences);

    float L = ((float) countOfLetters / (float) countOfWords) * 100;
    float S = ((float) countOfSentences / (float) countOfWords) * 100;

    // The Coleman-Liau formula
    int grade = round(0.0588 * L - 0.296 * S - 15.8);

    return grade;
}