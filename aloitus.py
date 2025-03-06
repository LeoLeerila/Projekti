import inquirer


valinnat = ["Aloita peli", "Lopeta peli"]

def aloitus():
    print("""\


          __|__
    *---o--(_)--o---*                _  _
                                   ( `   )_
       MIEHEN SALAINEN MATKA    (    )    `)
          THAIMAA             (_   (_ .  _) _)                       

       """)
    aloitus = input("Paina mitä vain aloittaaksesi: ")

    questions = [
        inquirer.List('valinta',
                      message="Valitse:",
                      choices=valinnat,  # Use the dynamically generated list
                      ),
    ]


    answers = inquirer.prompt(questions)

    if answers['valinta'] == "Aloita peli":
        print("Aloitetaan peli! Matka Thaimaahan alkaa...")

    else:
        print("Peli lopetetaan.")
        exit()

print("Sinun täytyy matkustaa Thaimaaseen ilman, että ylität CO2-budjettisi.")
aloitus()

