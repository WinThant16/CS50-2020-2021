#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //asking prompt for text
    string text = get_string("Input: ");

    int letters = 0;
    int words = 1;
    int sentences = 0;
    int length = strlen(text);

    //calculating letters
    for (int i = 0; i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    //calculating words
    for (int n = 0; n < length; n++)
    {
        if (isspace(text[n]))
        {
            words++;
        }
    }

    //calculating sentences
    for (int r = 0; r < length; r++)
    {
        if (text[r] == '.' || text[r] == '!' || text[r] == '?')
        {
            sentences++;
        }
    }

    float l = letters;
    float w = words;
    float s = sentences;

    //average letters per 100 words
    float L = (l * (100 / w));

    //average sentences per 100 words
    float S = (s * (100 / w));

    //Coleman-liau Formula
    float index = ((0.0588 * L) - (0.296 * S) - 15.8);

    //rounding off for whole number
    int grade = round(index);

    if (index >= 16)
    {
        printf("Grade 16+");
    }
    else if (index < 1)
    {
        printf("Before Grade 1");
    }
    else
    {
        printf("Grade %i", grade);
    }

    printf("\n");
}