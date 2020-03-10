#include "helpers.h"
#include <string.h>
#include <stdio.h>
#include <math.h>



// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for(int i = 0; i < height ;i++)
    {
        for(int j = 0; j < width;j++)
        {
        float avarage_decimals = ( (float )(image[i][j].rgbtRed) + ( (float) image[i][j].rgbtBlue) + ( (float)image[i][j].rgbtGreen) ) / 3;
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
    for(int i = 0; i < height ;i++)
    {
        for(int j = 0; j < width;j++)
        {
            float originalRed = image[i][j].rgbtRed ;
            float originalBlue =  image[i][j].rgbtBlue ;
            float originalGreen = image[i][j].rgbtGreen;

            float sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue;
            float sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue;
            float sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue;

            if(sepiaRed >255){
            sepiaRed = 255;}

            if(sepiaGreen >255){
            sepiaGreen = 255;}

            if(sepiaGreen >255){
            sepiaGreen = 255;}


            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
   RGBTRIPLE temp;
   
    for(int i = 0;i<height;i++)
    {
        for(int j = 0; j< width/2;j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width -j-1];
            image[i][width -j-1] = temp;
        }
    }
    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
