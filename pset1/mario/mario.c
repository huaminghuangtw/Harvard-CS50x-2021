#include <cs50.h>
#include <stdio.h>

void drawPyramid(int height);
void drawPyramid_recursive(int height, int level);

int main(void)
{
    // Prompt the user for the pyramid’s height, a positive integer between 1 and 8, inclusive
    int height;
    //do
    //{
    //    height = get_int("Height: ");
    //}
    do
    {
        printf("Height: ");
        scanf("%i", &height);
    }
    while (height > 8 || height < 1);

    // drawPyramid(height);
    drawPyramid_recursive(height, height);

    return 0;
}

void drawPyramid(int height)
{
    for (int level = 1; level <= height; ++level)
    {
        for (int column = height - level; column >= 1; --column)
        {
            printf(" "); // putchar(' ');
        }

        for (int column = 1; column <= level; ++column)
        {
            putchar('#'); // printf("#");
        }

        printf("  ");

        for (int column = 1; column <= level; ++column)
        {
            printf("#");
        }

        printf("\n");
    }
}

void drawPyramid_recursive(int height, int level)
{
    if (level == 0) // base case
    {
        return;
    }

    drawPyramid_recursive(height, level - 1);

    for (int column = height - level; column >= 1; --column)
    {
        printf(" "); // putchar(' ');
    }

    for (int column = 1; column <= level; ++column)
    {
        putchar('#'); // printf("#");
    }

    printf("  ");

    for (int column = 1; column <= level; ++column)
    {
        printf("#");
    }

    printf("\n");
}