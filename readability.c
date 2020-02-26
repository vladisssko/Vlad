#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string s =get_string("Text: ");
    int letter = 0;
    int words = 1;
    int sentence = 0;
    int n = strlen(s);

for (int i = 0; i < n;  i++)
{
//counting letters

    if (  isalnum(s[i])  )
        {
            letter++;
        }
    if (s[i] == ' ')
       {
           words++;
       }
        
    if (s[i] == '.' || s[i] == '!' || s[i] == '?')        
        {
            sentence++;
        }
}

    float L = ((float) letter*(100/(float) words));
    float S = ( sentence*(100/(float)words) );
    float Grade = 0.0588 * ( L) - 0.296 * ( S )  - 15.8 ;

    if (Grade < 16 && Grade >= 0)
    {
        printf("Grade %i\n", (int) round(Grade));
    }
    else if (Grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
}
