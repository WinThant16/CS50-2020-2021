from cs50 import get_int


def main():
    height = get_pos_int()
    i = 0
    j = 0
    k = 0
    for i in range(height):

        for j in range(height-i-1):
            print(" ", end="")
        for k in range(i+1):
            print("#", end="")
        
        print("  ", end="")
        
        for l in range(i+1):
            print("#", end="")
        print()
        

# verifying height between 0 and eight
def get_pos_int():
    # asking pyramid height
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break
    return height


main()