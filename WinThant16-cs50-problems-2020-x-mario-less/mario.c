#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int number;
    do
    {
        number = get_int("Height: ");
    }
    while (number < 1 || number > 8);

    //asking for pyramid height
    for (int i = 0; i < number; i++)
    {
        //space
        for (int j = number - 1; j > i; j--)
        {   
            printf(" ");
        }    
        //hash
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}