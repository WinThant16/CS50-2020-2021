#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{


    float change;
    int coins = 0;

    //asking amount of money
    do
    {
        change = get_float("Owed Money:");

    }
    while (change <= 0);
    
    //converting
    int cents = round(change * 100);
    int quarts = 0, dimes = 0, nickels = 0, pennies = 0;
    
    
    while (cents != 0)
    {   
        //total amount of nickels
        while (cents >= 25)
        {
            nickels = nickels + 1;
            cents = cents - 25;
        }
        while (cents >= 10)
        {
            dimes = dimes + 1;
            cents = cents - 10;
        }
        while (cents >= 5)
        {
            quarts = quarts + 1;
            cents = cents - 5;
        }
        while (cents >= 1)
        {
            pennies = pennies + 1;
            cents = cents - 1;
        }
    
    }
    coins = nickels + dimes + quarts + pennies;
    printf("Coins required: %i\n", coins);
}
    