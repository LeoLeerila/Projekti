import inquirer
from tietokanta import haeMaanTiedot, haePelaajanTiedot
from lentokone import laskeLennonPituus
import chalk

def lentokentat():
  pelaajanTiedot = haePelaajanTiedot(1)
  #id, co2_consumed, co2_budget, location, screen_name, time, km_total
  pelaajanTiedot = {
      "id": pelaajanTiedot[0],
      "co2_consumed": pelaajanTiedot[1],
      "co2_budget": pelaajanTiedot[2],
      "location": pelaajanTiedot[3],
      "screen_name": pelaajanTiedot[4],
      "time": pelaajanTiedot[5],
      "km_total": pelaajanTiedot[6]
  }
  print(pelaajanTiedot)

   

def valitseSeuraavaLentokentta(location):
  # Get the list of airports
  lentokentat = laskeLennonPituus(location, "*")

  maat = []
  for lentokentta in lentokentat:
      maa_tiedot = haeMaanTiedot("name", "iso_country", lentokentta["maa"])
      if maa_tiedot and len(maa_tiedot[0]) > 0:  # Ensure data exists
          maat.append(f"{maa_tiedot[0][0]} {chalk.red(f"-{round(lentokentta["co2Lennolta"], 2)} kg CO₂")}")  # Extract the first name

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

valitseSeuraavaLentokentta("EFHK")
lentokentat()