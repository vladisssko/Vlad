from cs50 import get_float

# propt user for input of change owed while input is number higher of 0

while True:
    dollars = get_float("change owed : ")
    if dollars >0:
        break
#input of dollars will be multiplied by 100 and rounded, in order to get cents 
coins = 0

cents = 0

cents = round(dollars * 100)

while True:
    if (cents >= 25):
        cents -= 25
        coins += 1
    else:
        break

while cents < 25: 
        if (cents >= 10):
            cents -= 10
            coins += 1
        else:
            break

            
while  cents <10: 
    if (cents >= 5):
        cents -= 5
        coins += 1
    else:
        break
        
coins += cents
        
print(coins)
    

