import inquirer
from tietokanta import haePelaajanTiedot

valinnat = ["Tarkastele tilastoja", "Lopeta peli"]

def voitto():
    print("""
          o  \\ o / _ o       __|   \\ /    |__      o _ \\ o /  o
         /|\\   |    /\\  ___\\o  \\o   |   o/   o/__  /\\    |   /|\\
         / \\  / \\  | \\ /)  |   ( \\ /o\\ / )   |  (\\ / |  / \\  / \\
         ONNEKSI OLKOON OLET SAAPUNUT THAIMAASEEN
       """)
    #lopetus = input("Paina ENTER-näppäintä jatkaaksesi: ")

    questions = [
        inquirer.List('valinta',
                      message="Valitse:",
                      choices=valinnat,  # Use the dynamically generated list
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers['valinta'] == "Tarkastele tilastoja":
        tiedot = haePelaajanTiedot(1)
        
        #print(f"{tiedot['id']}")
        print(f"käytetty co2 budjetti {tiedot['co2_consumed']}")
        print(f"koko co2 budjetti {tiedot['co2_budget']}")
        #print(f"{tiedot['location']}")
        #print(f"{tiedot['screen_name']}")
        print(f"aika lentäessä {tiedot['time']}")
        print(f"lentojen kokonais matka {tiedot['km_total']}")
        
        #lopetus = input("Paina ENTER-näppäintä lopettaaksesi: ")
        #exit()

    else:
        print("Peli lopetetaan.")
        #exit()

def havio():
    print("""

         /O\  
          |   
         / \  
         VALITETTAVASTI ET PÄÄSSYT THAIMAASEEN
       """)
    #lopetus = input("Paina ENTER-näppäintä jatkaaksesi: ")

    questions = [
        inquirer.List('valinta',
                      message="Valitse:",
                      choices=valinnat,  # Use the dynamically generated list
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers['valinta'] == "Tarkastele tilastoja":
        tiedot = haePelaajanTiedot(1)
        
        #print(f"{tiedot['id']}")
        print(f"käytetty co2 budjetti {tiedot['co2_consumed']} kg")
        print(f"koko co2 budjetti {tiedot['co2_budget']} kg")
        #print(f"{tiedot['location']}")
        #print(f"{tiedot['screen_name']}")
        print(f"aika lentäessä {tiedot['time']} h")
        print(f"lentojen kokonais matka {tiedot['km_total']} km")
        
        #lopetus = input("Paina ENTER-näppäintä lopettaaksesi: ")
        #exit()

    else:
        print("Peli lopetetaan.")
        #exit()


#lopetus()

