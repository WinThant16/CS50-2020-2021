#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //checking commandline argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    //checking if memory card is opened correctly
    if (file == NULL)
    {
        fprintf(stderr, "Can't open file %s\n", argv[1]);
        return 1;
    }


    //if opened correctly
    
    FILE *image;
    unsigned char *buffer = malloc(512); //allocates memory for buffer files
    int filecounter = 0; //to count number of jpg files
    char imgfile[filecounter]; //to save jpg files into a folder
    
    
    //while reading the file
    while (fread(buffer, 512, 1, file))
    {
        //what to do if jpg found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //close each individual jpg if they alr exist in loop
            if (filecounter > 0)
            {
                fclose(image);
            }

            //create file for jpg
            sprintf(imgfile, "%03d.jpg", filecounter);
            
            
            //run(open) image file 
            image = fopen(imgfile, "w");
            
            //if unable to detect jpg
            if (image == NULL)
            {
                fclose(file);
                free(buffer);
                fprintf(stderr, "Could not create jpg %s.\n", imgfile);
            }
            filecounter++;
        }    

        //write in file if jpgs detected
        if (filecounter > 0)
        {
            fwrite(buffer, 512, 1, image);
        }        
                
    }
    free(buffer);
    fclose(image);
    fclose(file);

    return 0;
}
