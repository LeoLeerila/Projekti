import inquirer
import random

from tietokanta import annakysymys, annavastaus, annakysymysVaihtoehto, haePelaajanTiedot, paivitaPelaajanTiedot
#from tietokanta import annakysymysVaihtoehto2
#from tietokanta import annakysymysVaihtoehto3


def kysymys():
    N = random.randint(1, 50)
    oikeavastaus = annavastaus(N)[0][0]
    kysymys = annakysymys(N)[0]
    #print(kysymys)
    #print(oikeavastaus)
    lista = [annakysymysVaihtoehto(N, 1)[0], annakysymysVaihtoehto(N, 2)[0], annakysymysVaihtoehto(N, 3)[0]]
    questions = [
        #"Tää on kyl paha..."
      inquirer.List('vastaus',
                        message= kysymys,
                        choices=lista)]
    answer = inquirer.prompt(questions)["vastaus"]
    #pprint(answer)
    #print(answer)
    if answer == oikeavastaus:
        pelaajantiedot = haePelaajanTiedot(1)
        paivitaPelaajanTiedot(1, "co2_budget", (pelaajantiedot["co2_budget"] + 75))
        print("oikea vastaus")#, answer["Tää"])

    else:
        print("väärä vastaus")

def palvelinKysymys():
    N = random.randint(1, 50)
    oikeavastaus = annavastaus(N)[0][0]
    kysymys = annakysymys(N)[0]
    #print(kysymys)
    #print(oikeavastaus)
    lista = [annakysymysVaihtoehto(N, 1)[0], annakysymysVaihtoehto(N, 2)[0], annakysymysVaihtoehto(N, 3)[0]]
    kysymykset = {
        "kysymys": kysymys,
        "mahdollisetVastaukset": lista,
        "oikeaVastaus": oikeavastaus
    }
    return kysymykset