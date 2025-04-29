import inquirer
from tietokanta import haeMaanTiedot, haePelaajanTiedot, haeMaanLentokentat, haePelaajanNykyinenMaa, paivitaPelaajanTiedot, haeLentokentanTiedot
from lentokone import laskeLennonPituus, lenna
import chalk
import random


def lentokentat(lahtoSijainti, pelaajanTiedot):
  # Get the list of airports
  lentokentatRaw = laskeLennonPituus(lahtoSijainti, "*")

  lentokentat = []
  for data in lentokentatRaw:
      lentokentan_tiedot = haeLentokentanTiedot("name", "ident", data["lentokentta"])
      if round(data["co2Lennolta"], 2) <= pelaajanTiedot["co2_budget"] - pelaajanTiedot["co2_consumed"]:
         if pelaajanTiedot["location"] != data['lentokentta']: 
          lentokentat.append((f"{lentokentan_tiedot[0]} {chalk.red(f"-{round(data["co2Lennolta"], 2)} kg CO₂")}", data['lentokentta']))
  print(f"Calculated routes to {len(lentokentat)} countries.")
  return lentokentat
   

def valitseSeuraavaLentokentta(location, pelaajanID):
  pelaajanTiedot = haePelaajanTiedot(pelaajanID)
  print("You are in", chalk.green(haePelaajanNykyinenMaa(pelaajanTiedot["location"])))
  print("You can emit a total of", chalk.green(pelaajanTiedot["co2_budget"]-pelaajanTiedot["co2_consumed"]), "kg CO₂")

  lentokenttaLista = lentokentat(location, pelaajanTiedot)
  if not lentokenttaLista:
     return
  # Create the question with dynamic choices
  questions = [
      inquirer.List('lentokentta',
                    message=f"Where would you like to fly? ({len(lentokenttaLista)})",
                    choices=lentokenttaLista,  # Use the dynamically generated list
                ),
  ]

  # Prompt the user
  answers = inquirer.prompt(questions)

  # Print the selected answer
  print("You selected:", answers["lentokentta"])

  lento = lenna(answers["lentokentta"], pelaajanTiedot["location"], 1, pelaajanTiedot["id"])

  return answers["lentokentta"]

def testiTehtava():
  questions = [
      inquirer.List('tehtava',
                    message="Choose a country:",
                    choices=[("The Earth is flat", 0), ("The earth is round", 1)]
                ),
  ]

  answers = inquirer.prompt(questions)
  print("You selected:", answers["tehtava"])
  if answers["tehtava"] == 1:
      print("Correct answer!")
      pelaajanTiedot = haePelaajanTiedot(1)
      paivitaPelaajanTiedot(1, "co2_budget", (pelaajanTiedot["co2_budget"]+random.randint(200, 500)))
  else:
     print(chalk.red("Wrong answer :("))

#valitseSeuraavaLentokentta(haePelaajanTiedot(1)["location"])