import inquirer
from tietokanta import laskeLennonPituus

lentokentat = laskeLennonPituus((53.2400016784668, 50.375), "EU")

for lentokentta in lentokentat:
    print(lentokentta["maa"])

questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            ),
]
answers = inquirer.prompt(questions)