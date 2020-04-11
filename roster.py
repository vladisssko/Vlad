import sys
import csv
from cs50 import SQL
from cs50 import get_string

# open sdutents.db
open("students.db" , "r").close()

db = SQL("sqlite:///students.db")

if len(sys.argv) != 2:
    print("Usage: python roster.py Gryffindor")
    sys.exit(1)


o= db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first;", sys.argv[1])

for i in range(len(o)):
    print(o[i]["first"], end= " ")
    if o[i]["middle"] != None :
        print(o[i]["middle"], o[i]["last"], end =",")
        print(" born", o[i]["birth"])
    else: 
        print(o[i]["last"], end = ",")
        print(" born", o[i]["birth"])
        