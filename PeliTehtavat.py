import random


randomLuku = random.randint(1,4)
def tehava(randomLuku):
    if randomLuku == 1:
        kysy = int(input("Mikä on 1+1? "))
        if kysy == 2:
            print("oikein")

    elif randomLuku == 2:
        kysy = int(input("Mikä on 1+2? "))
        if kysy == 3:
            print("oikein")

    elif randomLuku == 3:
        kysy = int(input("Mikä on 1+3? "))
        if kysy == 4:
            print("oikein")

    elif randomLuku == 4:
        kysy = int(input("Mikä on 1+4? "))
        if kysy == 5:
            print("oikein")

tehava(randomLuku)