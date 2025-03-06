import inquirer

from tietokanta import annakysymys
from tietokanta import annavastaus
from tietokanta import annakysymysVaihtoehto1
from tietokanta import annakysymysVaihtoehto2
from tietokanta import annakysymysVaihtoehto3

oikeavastaus = annavastaus(1)[0][0]
kysymys = annakysymys(1)[0]
print(kysymys)
lista = [annakysymysVaihtoehto1(1)[0], annakysymysVaihtoehto2(1)[0], annakysymysVaihtoehto3(1)[0]]
questions = [
  inquirer.List('interests',
                    message= '"Tää on kyl paha..."',
                    choices=lista)]
answer = inquirer.prompt(questions)
#pprint(answer)

if answer == oikeavastaus:
    print("Kyl se on")#, answer["Tää"])


