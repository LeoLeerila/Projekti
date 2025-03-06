import mysql.connector
import chalk
import inquirer

from tietokanta import annakysymys
from tietokanta import annavastaus
from tietokanta import annakysymysVaihtoehto1
from tietokanta import annakysymysVaihtoehto2
from tietokanta import annakysymysVaihtoehto3

oikeavastaus = annavastaus(1)[0][0]
kysymykset = annakysymys(1)
kyssärit  = []


if kysymykset and len(maa_tiedot[0]) > 0:  # Ensure data exists
        kyssärit.append(
            f"{maa_tiedot[0][0]} {chalk.red(f"-{round(lentokentta["co2Lennolta"], 2)} CO₂")}")  # Extract the first name
#annakysymys(1)
#vastaus = input("Kirjoita vastaus: ")
#if vastaus in oikeavastaus:
#    print("oikein")
#elif vastaus not in oikeavastaus:
#    print("väärin")

# Create the question with dynamic choices
  questions = [
      inquirer.List('maa',
                    message="Choose a country:",
                    choices=maat,  # Use the dynamically generated list
                ),
  ]

  # Prompt the user
  answers = inquirer.prompt(questions)

  # Print the selected answer
  print("You selected:", answers["maa"])

valitseSeuraavaLentokentta()