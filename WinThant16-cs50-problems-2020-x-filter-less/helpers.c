#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = roundf((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.000);
            
            
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
    
    return;
}


// Convert image to sepia

//limit for sepia values
int limit(int n)
{
    if (n > 255)
    {
        n = 255;
    }
    return n;
}


void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    
    
    int sepiablue;
    int sepiared;
    int sepiagreen;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiablue = limit(round((0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue)));
            
            sepiared = limit(round((0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue)));
            
            sepiagreen = limit(round((0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue)));
        
            
            image[i][j].rgbtRed = sepiared;
            image[i][j].rgbtBlue = sepiablue;
            image[i][j].rgbtGreen = sepiagreen;
            
        }
    }
    
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //temporary array of 3 where swap[0] is for red, swap[1] is for blue, swap[2] is for green
    int swap[3];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++) //this is because u only need to swap half of one sie of the image
        {
            //swap array stores original half width of the image
            swap[0] = image[i][j].rgbtRed;
            swap[1] = image[i][j].rgbtBlue;
            swap[2] = image[i][j].rgbtGreen;
            
            
            
            //swap one side
            image[i][j].rgbtRed = image[i][(width - j) - 1].rgbtRed;
            image[i][j].rgbtBlue = image[i][(width - j) - 1].rgbtBlue;
            image[i][j].rgbtGreen = image[i][(width - j) - 1].rgbtGreen;
            
            //swap the other side
            image[i][(width - j) - 1].rgbtRed = swap[0];
            image[i][(width - j) - 1].rgbtBlue = swap[1];
            image[i][(width - j) - 1].rgbtGreen = swap[2];
            
            
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    float countblock; //counts each surrounding pixel
    RGBTRIPLE org[height][width]; // original table to store colors
    //1
    int totalGreen;
    int totalBlue;
    int totalRed;
    //1 - adding total values of each color from surrouning pixels
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            totalGreen = 0;
            totalBlue = 0; 
            totalRed = 0;
            countblock = 0.000;
            //counting values of pixel and considering edges
            for (int h_edge = -1; h_edge < 2; h_edge++)
            {
                if (i + h_edge < 0 || i + h_edge > height - 1)
                {
                    continue;
                    
                }
                for (int w_edge = -1; w_edge < 2; w_edge++)
                {
                    if (j + w_edge < 0 || j + w_edge > width - 1)
                    {
                        continue;
                    }
                    
                    totalGreen += image[i + h_edge][j + w_edge].rgbtGreen;
                    totalBlue += image[i + h_edge][j + w_edge].rgbtBlue;
                    totalRed += image[i + h_edge][j + w_edge].rgbtRed;
                    countblock++;
                    
                    
                    
                }
            }
            //converts colors from the table
            org[i][j].rgbtGreen = round(totalGreen / countblock);
            org[i][j].rgbtBlue = round(totalBlue / countblock);
            org[i][j].rgbtRed = round(totalRed / countblock);
        }
        
        
    }
    //changes values of the image so that they are equal to the colors from the table
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtGreen = org[i][j].rgbtGreen;
            image[i][j].rgbtBlue = org[i][j].rgbtBlue;
            image[i][j].rgbtRed = org[i][j].rgbtRed;
        }
    }
    
    
    return;
}
