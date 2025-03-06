import inquirer
from tietokanta import haePelaajanTiedot

valinnat = ["Tarkastele tilastoja", "Lopeta peli"]

def lopetus():
    print("""
          o  \\ o / _ o       __|   \\ /    |__      o _ \\ o /  o
         /|\\   |    /\\  ___\\o  \\o   |   o/   o/__  /\\    |   /|\\
         / \\  / \\  | \\ /)  |   ( \\ /o\\ / )   |  (\\ / |  / \\  / \\
         ONNEKSI OLKOON OLET SAAPUNUT THAIMAASEEN
       """)
    lopetus = input("Paina ENTER-näppäintä jatkaaksesi: ")

    questions = [
        inquirer.List('valinta',
                      message="Valitse:",
                      choices=valinnat,  # Use the dynamically generated list
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers['valinta'] == "Tarkastele tilastoja":
        haePelaajanTiedot()
        lopetus = input("Paina ENTER-näppäintä lopettaaksesi: ")
        exit()

    else:
        print("Peli lopetetaan.")
        exit()


lopetus()

