import mysql.connector
from tietokanta import annakysymys
from tietokanta import annavastaus

oikeavastaus = annavastaus(1)[0][0]

annakysymys(1)
vastaus = input("Kirjoita vastaus: ")
if vastaus in oikeavastaus:
    print("oikein")
elif vastaus not in oikeavastaus:
    print("väärin")

