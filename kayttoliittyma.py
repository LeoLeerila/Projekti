import inquirer
from tietokanta import haeMaanTiedot, haePelaajanTiedot, haeMaanLentokentat, haePelaajanNykyinenMaa, paivitaPelaajanTiedot
from lentokone import laskeLennonPituus, lenna
import chalk
import random


def lentokentat(lahtoSijainti):
  # Get the list of airports
  lentokentat = laskeLennonPituus(lahtoSijainti, "*")

  maat = []
  for lentokentta in lentokentat:
      maa_tiedot = haeMaanTiedot("name", "iso_country", lentokentta["maa"])
      
      if maa_tiedot and len(maa_tiedot[0]) > 0 and haeMaanLentokentat(lentokentta["maa"]):  # Ensure data exists
          if round(lentokentta["co2Lennolta"], 2) <= haePelaajanTiedot(1)["co2_budget"] - haePelaajanTiedot(1)["co2_consumed"]:
            if haePelaajanTiedot(1)["location"] != haeMaanLentokentat(lentokentta["maa"])[0]:
              maat.append((f"{maa_tiedot[0][0]} {chalk.red(f"-{round(lentokentta["co2Lennolta"], 2)} kg CO₂")}", haeMaanLentokentat(lentokentta["maa"])))
  print(f"Calculated routes to {len(lentokentat)} countries.")
  return maat
   

def valitseSeuraavaLentokentta(location):
  pelaajanTiedot = haePelaajanTiedot(1)
  print("You are in", chalk.green(haePelaajanNykyinenMaa(pelaajanTiedot["location"])))
  print("You can emit a total of", chalk.green(pelaajanTiedot["co2_budget"]-pelaajanTiedot["co2_consumed"]), "kg CO₂")

  maat = lentokentat(location)
  if not maat:
     return
  # Create the question with dynamic choices
  questions = [
      inquirer.List('maa',
                    message=f"Where would you like to fly? ({len(maat)})",
                    choices=maat,  # Use the dynamically generated list
                ),
  ]

  # Prompt the user
  answers = inquirer.prompt(questions)

  # Print the selected answer
  print("You selected:", answers["maa"][0])

  lento = lenna(answers["maa"][0], haePelaajanTiedot(1)["location"], 1, 1)
  print(lento)

  return answers["maa"][0]

def testiTehtava():
  questions = [
      inquirer.List('tehtava',
                    message="Choose a country:",
                    choices=[("Maapallo on litteä", 0), ("Maapallo on pyöreä", 1)]
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