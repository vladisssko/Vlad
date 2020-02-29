#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
// if comand linde argument is not 1 then print : insert command line argument  


    if (argc != 2)
   {
       printf("Usage: ./caesar key\n");
       return 1;
   }       
   for (int i = 0, n = strlen(argv[1]); i < n; i++)
  
   
   if(isdigit (argv[1][i]) == false)
{
   printf("Usage: ./caesar key\n");
   return 1; 
}
    string s = get_string("plaintext:");
   
    printf("ciphertext:");
    
    int k = atoi (argv[1]);
    for (int i = 0; i < strlen(s); i++)
    if (isalpha(s[i]) != 0) 
    {
       
    if (s[i]  > ('Z') )
     {
     printf("%c",(s[i]+ k -97)% 26 + 97 );
     }
    else 
    {
    printf("%c",(s[i]+ k -65)% 26 + 65 );
    }
    
    }
    else 
    {
        printf("%c",s[i]);
    }
   
    
    
printf("\n");
}