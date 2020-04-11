import sys
import csv
from cs50 import SQL
from cs50 import get_string


# open sdutents.db
open("students.db" , "w").close()

db = SQL("sqlite:///students.db")
# Create table srudents in database students.db
db.execute("CREATE TABLE students (first TEXT, middle TEXT,last TEXT,house TEXT, birth NUMERIC) ")

# Check for correct number of args
if len(sys.argv) != 2:
    print("Usage: python import.py characters.csv")
    sys.exit(1)


with open(sys.argv[1], "r") as file :
    reader = csv.DictReader(file)

    for row in reader:

        m  = row["name"].split()

        if len(m) == 3:
            name[0] = m[0]
            middle = m[1]
            name[1] = m[2]

        else:
            name = row["name"].split()
            middle = None

        house = row["house"]
        birth = int(row["birth"])

        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (? , ? , ?,?,?) ",
            name[0], middle, name[1], house, birth)
