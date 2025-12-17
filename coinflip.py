import random

def coin_flipping():
    coinside = ""
    coin = random.randint(1,2)
    if coin == 1:
        coinside = "Heads :coin:"
    else:
        coinside = "Tails :coin:"
    return coinside
