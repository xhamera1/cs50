#include "helpers.h"
#include <math.h>

int min(int a, int b) {
    return (a < b) ? a : b;
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i=0;i<height;++i){
        for(int j=0;j<width;++j){
            double average=(image[i][j].rgbtBlue+image[i][j].rgbtRed+image[i][j].rgbtGreen)/3.0;
            int ave=round(average);
            image[i][j].rgbtBlue = ave;
            image[i][j].rgbtRed = ave;
            image[i][j].rgbtGreen = ave;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i=0;i<height;++i){
        for(int j=0;j<width;++j){

            int sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(0.349 * image[i][j].rgbtRed +  0.686* image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534* image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = min(255, sepiaRed);
            image[i][j].rgbtGreen = min(255, sepiaGreen);
            image[i][j].rgbtBlue = min(255, sepiaBlue);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i=0;i<height;++i){
        for(int j=0;j<width/2;j++){
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1]= temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            int redSum = 0, greenSum = 0,blueSum = 0;
            int count = 0;
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width){
                        redSum += copy[ni][nj].rgbtRed;
                        greenSum += copy[ni][nj].rgbtGreen;
                        blueSum += copy[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }
            image[i][j].rgbtRed = round(redSum / (float)count);
            image[i][j].rgbtGreen = round(greenSum / (float)count);
            image[i][j].rgbtBlue = round(blueSum / (float)count);
        }
    }
}
