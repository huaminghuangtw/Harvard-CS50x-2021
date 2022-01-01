#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

const int BLOCK_SIZE = 512;
typedef uint8_t BYTE;

bool isJPEGs(const BYTE *buffer);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open card.raw
    FILE *infile = fopen(argv[1], "r");
    if (!infile)
    {
        fprintf(stderr, "ERROR - Could not open %s.\n", argv[1]);
        return 1;
    }

    BYTE *buffer = malloc(BLOCK_SIZE);   // or BYTE buffer[BLOCK_SIZE];
    int countOfImages = 0;
    FILE *img = NULL;
    char filename[10];

    while (fread(buffer, sizeof(buffer), 1, infile))
    {
        if (isJPEGs(buffer))
        {
            // close previous JPEG file if it exists
            if (countOfImages > 0)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", countOfImages);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(infile);
                free(buffer);
                fprintf(stderr, "ERROR - Could not create output JPG: %s\n", filename);
            }

            countOfImages++;
        }

        // If JPEG has been found, keep writing to file
        if (countOfImages > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }
    }

    fclose(infile);
    fclose(img);
    free(buffer);

    return 0;
}

bool isJPEGs(const BYTE *buffer)
{
    return (buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0);
    // The expression buffer[3] & 0xf0) == 0xe0 to check the fourth byte is equivalent to:
    // buffer[3] == 0xe0 || buffer[3] == 0xe1 || ... || buffer[3] == 0xef
}