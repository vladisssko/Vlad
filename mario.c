#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get and validate user input
    int n;

    do
    {
        n = get_int("Height: "); 
    }
    while (n < 1 || n > 8);

    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n - i;j++)
        {
        printf(" "); 
        }  
            for (int k = 1; k < i + 1 ;k++)
        {
            printf("#");
            
        }   
        
        
       printf("\n");
     
    }
}
