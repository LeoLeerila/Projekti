import inquirer

from tietokanta import haePelaajanTiedot

valinnat = ["Tarkastele tilastoja", "Lopeta peli"]

def aloitus():
    print("""
          o  \\ o / _ o       __|   \\ /    |__      o _ \\ o /  o
         /|\\   |    /\\  ___\\o  \\o   |   o/   o/__  /\\    |   /|\\
         / \\  / \\  | \\ /)  |   ( \\ /o\\ / )   |  (\\ / |  / \\  / \\
         VOITIT PELIN
       """)

    questions = [
        inquirer.List('valinta',
                      message="Valitse:",
                      choices=valinnat,  # Use the dynamically generated list
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers['valinta'] == "Tarkastele tilastoja":
        haePelaajanTiedot()

    else:
        print("Peli lopetetaan.")
        exit()


aloitus()

