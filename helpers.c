#include "helpers.h"
#include <string.h>
#include <stdio.h>
#include <math.h>



// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
  
    for(int i = 0; i < height-1;i++)
    {
        for(int j = 0; j < width-1;j++)
        {
        float avarage_decimals = (image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3;  
        int avarage =  round(avarage_decimals);
        image[i][j].rgbtRed = avarage;
        image[i][j].rgbtBlue = avarage;
        image[i][j].rgbtGreen = avarage;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
