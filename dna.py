import sys
import csv 
from cs50 import get_string

# Check for correct number of args
if len(sys.argv) != 3:
    print("Usage: dna.py database.csv sequence.txt")
    sys.exit(1)

database = sys.argv[1]
sequence = sys.argv[2]

# read possible STRs to be compared vs DNA
with open(database, 'r') as f:
    reader = csv.reader(f)
    for raw in reader:
        STRs = raw[1:]
        break
# read dna sequence in to list
with open( sequence, 'r') as k:
        data = k.read()

#find the longest run of each STR in DNA        
correctSTR=[]
for j in range(len(STRs)):
    count,max_count = 0,0
    for x in range(len(data)) :
            if data[x:x+len(STRs[j])] == STRs[j]: 
                while data[x:x+len(STRs[j])] == STRs[j]:
                    count +=1
                    x += len(STRs[j])
                    if count > max_count:
                        max_count = count
                else:
                    count = 0
    correctSTR.append(max_count)

#compare DNA STRs with database and print name if match, if no match print no match
with open(database, 'r') as f:
    reader = csv.reader(f)
    next(f)
    people = []
    for row in reader:
        people.append(row)

#converting strings in list to integers
for j in range(0,len(people)):
    for i in range(1, len(people[j])): 
        people[j][i] = int(people[j][i])  

#comparing int STRs from databse  vs int STRs from DNA
for o in range(len(people)):
    no_match = False
    if people[o][1:] == correctSTR:
        print(people[o][0])
        break
    else:
        no_match = True

if no_match == True:
        print("no match")        

