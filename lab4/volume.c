// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open input/output files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (!input)
    {
        printf("ERROR - Could not open %s.\n", argv[1]);
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (!output)
    {
        printf("ERROR - Could not open %s.\n", argv[2]);
        return 1;
    }

    float factor = atof(argv[3]);

    // Copy header from input file to output file
    BYTE header[HEADER_SIZE];
    fread(header, sizeof(header), 1, input);
    fwrite(header, sizeof(header), 1, output);

    // Read samples from input file and write updated data to output file
    int16_t buffer;
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    return 0;
}
