from cs50 import get_float


def main():
    change = get_money()
    
    cents = round(change * 100)
    quarts = 0
    dimes = 0
    nickels = 0
    pennies = 0
    coins = 0
    
    while cents != 0:
        while cents >= 25:
            nickels = nickels + 1
            cents = cents - 25
            if cents < 25:
                break
        while cents >= 10:
            dimes = dimes + 1
            cents = cents - 10
            if cents < 10:
                break
        while cents >= 5:
            quarts = quarts + 1
            cents = cents - 5
            if cents < 5:
                break
        while cents >= 1:
            pennies = pennies + 1
            cents = cents - 1
            if cents < 0:
                break
            
    coins = nickels + dimes + quarts + pennies
    print("Coins required: ", coins)


def get_money():
    # asking owed money
    while True:
        change = get_float("Owed Money: ")
        if change > 0:
            break
    return change


main()

