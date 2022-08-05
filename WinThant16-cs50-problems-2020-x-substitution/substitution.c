#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>


int main(int argc, string argv[])
{
    //checking command-line argument

    if (argc != 2)
    {
        if (argc == 1)
        {
            printf("Missing command-line argument.\n");
            return 1;
        }
        else
        {
            printf("Invalid command line argument.");
            return 1;
        }
    }
    if (argc == 2)
    {
        if (strlen(argv[1]) == 26)
        {
            //checking strings
            for (int i = 0; i < strlen(argv[1]); i++)
            {
                if (!isalpha(argv[1][i]))   //if they contain non-alphabets
                {
                    printf("Key must contain 26 characters.\n");
                    return 1;
                }
                for (int j = i + 1; j < strlen(argv[1]); j++)
                {
                    if (toupper(argv[1][i]) == toupper(argv[1][j])) //if they contain repeated char
                    {
                        printf("Key must not contain repeated alphabets.\n");
                        return 1;
                    }
                }
            }
            //uppercase & lowercase
            string pt = get_string("plaintext: ");
            printf("ciphertext: ");
            string alpha = "abcdefghijklmnopqrstuvwxyz";
            int count = strlen(pt);
            string cipher = argv[1];
            char ct[count];

            for (int i = 0; i < count; i++)
            {
                if (isupper(pt[i]) != 0) //if character is uppercase
                {
                    for (int j = 0; j < 26; j++)
                    {
                        if (alpha[j] == tolower(pt[i]))
                        {
                            ct[i] = toupper(cipher[j]);
                            break;
                        }
                    }
                }
                else if (islower(pt[i]) != 0) //if character is lowercase
                {
                    for (int j = 0; j < 26; j++)
                    {
                        if (alpha[j] == pt[i])
                        {
                            ct[i] = tolower(cipher[j]);
                            break;
                        }
                    }
                }
                else if (!isalpha(pt[i]))
                {
                    ct[i] = pt[i];
                }
                else
                {
                    ct[i] = pt[i];
                }
            }

            printf("%s\n", ct);
            return 0;

        }
        else
        {
            printf("Key must be 26 characters long.\n");
            return 1;
        }
    }
    else
    {
        return 1;
    }

}