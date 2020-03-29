from cs50 import get_string

s = get_string("Text: ")
letter = 0
words = 1
sentence = 0
string_lenght=len(s)

for i in range (string_lenght):
# counting letters, words and sentences
    if s[i].isalnum():
        letter +=1
        
    if s[i] == ' ':
        words += 1
        
    if  s[i] == '.' or s[i] == '!' or s[i] == '?':
        sentence += 1
print(letter, words, sentence)        
L = letter * (100/ words) 
S = sentence*(100/words) 
Grade = 0.0588 * ( L) - 0.296 * ( S )  - 15.8 

if Grade < 16 and Grade >= 0:
    print("Grade", round(Grade));
    
elif Grade >= 16:
    print("Grade 16+\n")
    
else: 
    print("Before Grade 1\n")
    
