from flask import Flask, request

from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot, paivitaPelaajanTiedot
from lopetus import voitto, havio
from kayttoliittyma import valitseSeuraavaLentokentta
from PeliTehtavat import kysymys

app = Flask(__name__)

#Tietokannan funktiot
@app.route("/PelaajanTiedot/hae/")#http://127.0.0.1:3000/PelaajanTiedot/hae/?pelaajanID=1
def hae():
    args = request.args
    vastaus = haePelaajanTiedot(args.get("pelaajanID"))
    return vastaus

@app.route("/PelaajanTiedot/nollaa/")#http://127.0.0.1:3000/PelaajanTiedot/nollaa/?pelaajanID=1
def nollaa():
    args = request.args
    nollaaPelaajanTiedot(args.get("pelaajanID"))
    return f"pelaajan {args.get("pelaajanID")} tiedot päivitetty"

@app.route("/PelaajanTiedot/paivita/")#http://127.0.0.1:3000/PelaajanTiedot/paivita/?pelaajanID=1&paivitettavaTieto=co2_consumed&tiedonArvo=100
def paivita():
    args = request.args
    print(args)
    paivitaPelaajanTiedot(args.get("pelaajanID"), args.get("paivitettavaTieto"), args.get("tiedonArvo"))
    return f"Pelaajan {args.get("pelaajanID")} tieto {args.get("paivitettavaTieto")} muutettu {args.get("tiedonArvo")}"

#Lopetus funktiot
@app.route("/Lopetus/voitto/")
def Lopetusvoitto():
    #voitto()
    return "Pelaaja voitti pelin"

@app.route("/Lopetus/havio/")
def Lopetushavio():
    #havio()
    return "Pelaaja hävisi pelin"

if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)