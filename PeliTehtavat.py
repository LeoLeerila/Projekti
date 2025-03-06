import os
import sys
from pprint import pprint

sys.path.append(os.path.realpath("."))

import inquirer

from tietokanta import annakysymys
from tietokanta import annavastaus
from tietokanta import annakysymysVaihtoehto1
from tietokanta import annakysymysVaihtoehto2
from tietokanta import annakysymysVaihtoehto3

oikeavastaus = annavastaus(1)[0][0]
kysymys = annakysymys(1)[0]
print(kysymys)
print(oikeavastaus)
questions = [
  inquirer.List('interests',
                    message= '"Tää on kyl paha..."',
                    carousel=True,
                    choices=[annakysymysVaihtoehto1(1)[0], annakysymysVaihtoehto2(1)[0], annakysymysVaihtoehto3(1)[0]])]
#answer = inquirer.prompt(questions)
#pprint(answer)
vastaus = input("kirjoita vastaus: ")
if vastaus == oikeavastaus:
    print("Kyl se on")#, answer["Tää"])


