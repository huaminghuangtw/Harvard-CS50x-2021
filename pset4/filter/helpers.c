#include <math.h>
#include <string.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            BYTE new_pixel = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            image[i][j].rgbtBlue = new_pixel;
            image[i][j].rgbtGreen = new_pixel;
            image[i][j].rgbtRed = new_pixel;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; ++i)
    {
        int mid_pixel = ceil(width / 2);
        for (int j = 0; j < mid_pixel; ++j)
        {
            BYTE temp;

            temp = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][(width - 1) - j].rgbtBlue;
            image[i][(width - 1) - j].rgbtBlue = temp;

            temp = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][(width - 1) - j].rgbtGreen;
            image[i][(width - 1) - j].rgbtGreen = temp;

            temp = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][(width - 1) - j].rgbtRed;
            image[i][(width - 1) - j].rgbtRed = temp;
        }
    }

    return;
}

// Blur image (3 x 3 box blur)
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image_copy[height][width];
    memcpy(image_copy, image, sizeof(RGBTRIPLE) * height * width);

    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            int sum[3] = {0};
            float counter = 0.0;
            // Note that counter cannot be integer type, otherwise the computation of averages below will go wrong! (truncated integer problem)

            for (int k = (i - 1); k <= (i + 1); ++k)
            {
                for (int l = (j - 1); l <= (j + 1); ++l)
                {
                    if (k < 0 || l < 0 || k >= height || l >= width)
                    {
                        continue;
                    }

                    sum[0] += image_copy[k][l].rgbtBlue;
                    sum[1] += image_copy[k][l].rgbtGreen;
                    sum[2] += image_copy[k][l].rgbtRed;

                    counter++;
                }
            }

            image[i][j].rgbtBlue = round(sum[0] / counter);
            image[i][j].rgbtGreen = round(sum[1] / counter);
            image[i][j].rgbtRed = round(sum[2] / counter);
        }
    }

    return;
}

// Detect horizontal/vertical edges using Sobel operator
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image_copy[height][width];
    memcpy(image_copy, image, sizeof(RGBTRIPLE) * height * width);

    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int Gy[3][3] = {
        {-1,-2,-1},
        { 0, 0, 0},
        { 1, 2, 1}
    };

    for (int i = 0; i < height; ++i)
    {
        for (int j = 0; j < width; ++j)
        {
            int sumX[3] = {0};
            int sumY[3] = {0};

            int result[3] = {0};

            for (int k = (i - 1), x = 0; k <= (i + 1); ++k, ++x)
            {
                for (int l = (j - 1), y = 0; l <= (j + 1); ++l, ++y)
                {
                    if (k < 0 || l < 0 || k >= height || l >= width)
                    {
                        continue;
                    }

                    sumX[0] += image_copy[k][l].rgbtBlue * Gx[x][y];
                    sumX[1] += image_copy[k][l].rgbtGreen * Gx[x][y];
                    sumX[2] += image_copy[k][l].rgbtRed * Gx[x][y];

                    sumY[0] += image_copy[k][l].rgbtBlue * Gy[x][y];
                    sumY[1] += image_copy[k][l].rgbtGreen * Gy[x][y];
                    sumY[2] += image_copy[k][l].rgbtRed * Gy[x][y];
                }
            }

            for (int idx = 0; idx < 3; ++idx)
            {
                result[idx] = round(sqrt(sumX[idx] * sumX[idx] + sumY[idx] * sumY[idx]));
            }

            image[i][j].rgbtBlue = (result[0] > 255) ? 255 : result[0];
            image[i][j].rgbtGreen = (result[1] > 255) ? 255 : result[1];
            image[i][j].rgbtRed = (result[2] > 255) ? 255 : result[2];
        }
    }

    return;
}
