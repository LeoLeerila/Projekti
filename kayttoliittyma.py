import inquirer
from tietokanta import laskeLennonPituus, haeMaanTiedot
import chalk


def valitseSeuraavaLentokentta():
  # Get the list of airports
  lentokentat = laskeLennonPituus((53.2400016784668, 50.375), "EU")

  maat = []
  for lentokentta in lentokentat:
      maa_tiedot = haeMaanTiedot("name", "iso_country", lentokentta["maa"])
      if maa_tiedot and len(maa_tiedot[0]) > 0:  # Ensure data exists
          maat.append(f"{maa_tiedot[0][0]} {chalk.red(f"-{round(lentokentta["co2Lennolta"]/100, 2)} CO₂")}")  # Extract the first name

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