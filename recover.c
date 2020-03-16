#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    if (argc != 2)

{
    printf("Usage: ./recover image\n");
return 1;
}
//open file- memory card for reading 
FILE *inptr = fopen(argv[1], "r");

if(inptr == NULL)
{
    return 1;
}


int no_jpeg = 0;
unsigned char bytebuffer[512];
char filename[8];
FILE *image;
bool first_jpeg_found = false;

//go trought each chunk of 512 bytes until reaches end of the card 
while (fread (bytebuffer, 1, 512, inptr) ==512 )
{
    
//check if its JPEg header - has defined first 3 bytes = 1st jpeg 
if (bytebuffer[0] == 0xff && bytebuffer[1] == 0xd8 && bytebuffer[2] == 0xff ) 
    {
        
        
       first_jpeg_found = true;
       sprintf(filename, "%03i.jpg",no_jpeg); //prepise filename podla formatu xxx.jpg
       image = fopen(filename, "w"); //otvori xxx.jpg
       fwrite(bytebuffer, 1, 512, image); //starts writing in to xxx.jpg
        no_jpeg++; //first jpeg found increase no_jpeg value by 1

        
        
        printf("%i\n ", no_jpeg);
       }
       else //jpeg header not found 
       
       if (first_jpeg_found==true) //if header already found for 1st jpeg 
       {
           fwrite(bytebuffer, 1, 512, image); //continues writing in to fist jpeg
           
       }
       
}

fclose(image);
fclose(inptr);
}