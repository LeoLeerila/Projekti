import inquirer
from tietokanta import haeMaanTiedot, haePelaajanTiedot, haeMaanLentokentat, haePelaajanNykyinenMaa
from lentokone import laskeLennonPituus, lenna
import chalk

def lentokentat(lahtoSijainti):
  # Get the list of airports
  lentokentat = laskeLennonPituus(lahtoSijainti, "*")

  maat = []
  for lentokentta in lentokentat:
      maa_tiedot = haeMaanTiedot("name", "iso_country", lentokentta["maa"])
      if maa_tiedot and len(maa_tiedot[0]) > 0:  # Ensure data exists
          if round(lentokentta["co2Lennolta"], 2) <= haePelaajanTiedot(1)["co2_budget"]:
            if haePelaajanTiedot(1)["location"] != haeMaanLentokentat(lentokentta["maa"])[0]:
              maat.append((f"{maa_tiedot[0][0]} {chalk.red(f"-{round(lentokentta["co2Lennolta"], 2)} kg CO₂")}", haeMaanLentokentat(lentokentta["maa"])))  # Extract the first name
  return maat
   

def valitseSeuraavaLentokentta(location):
  pelaajanTiedot = haePelaajanTiedot(1)
  print(haePelaajanNykyinenMaa(pelaajanTiedot["location"]))

  maat = lentokentat(location)
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
  print("You selected:", answers["maa"][0])

  print(lenna(answers["maa"][0], haePelaajanTiedot(1)["location"], 1, 1))

valitseSeuraavaLentokentta("EFHK")