from cs50 import get_int

def main():
    
    i = get_correct_int()
    for a in range(i):
        for b in range(i-a-1):
            print(" ", end ="")
           
        for c in range(a+1):
            print("#", end="")
        print()
            
def get_correct_int():    
    while True:
        height = get_int("Height: ")
        if height>0 and height<9: 
            break
    return height
main()   
