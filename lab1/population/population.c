#include <cs50.h>
#include <stdio.h>


int main(void)
{
    // TODO: Prompt for start size
    int startSize;
    do
    {
        startSize = get_int("Please specify the start size (>= 9): \n");
    }
    while (startSize < 9);

    // TODO: Prompt for end size
    int endSize;
    do
    {
        endSize = get_int("Please specify the end size (>= start size): \n");
    }
    while (endSize < startSize);

    // TODO: Calculate number of years until we reach threshold
    int n = 0;
    int intermediateSize = startSize;
    while (intermediateSize < endSize)
    {
        intermediateSize = intermediateSize + (int)(intermediateSize / 3) - (int)(intermediateSize / 4); // cast floats to integers
        n++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", n);

    return 0;
}