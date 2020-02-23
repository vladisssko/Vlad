#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main (void)
{
    float dollars;
// propt user for input of change owed while input is number higher of 0
    do 
    {
    dollars =get_float("change owed ?");
    }

    while (dollars <0);
// input of dollars will be multiplied by 100 and rounded, in order to get cents     
    int cents;
    cents = round(dollars *100);


    int coins = 0;
    while (cents >=25)
    {
    cents -=25;
    coins++;
    }

 while (cents >=10)
    {
    cents -=10;
    coins++;
    }

 while (cents >=5)
    {
    cents -=5;
    coins++;
    }

    coins +=cents;
 


    printf("%i",coins);

    }
