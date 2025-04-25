from flask import Flask, request

from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot, paivitaPelaajanTiedot
from lopetus import voitto, havio
from kayttoliittyma import valitseSeuraavaLentokentta
from PeliTehtavat import kysymys

app = Flask(__name__)

#tietokannan funktiot funcHaePelaajanTiedot funcNollaaPelaajanTiedot
#app.add_url_rule("/tietokanta/haePelaajanTiedot/<int:pelaajanID>", endpoint="PelaajanTiedot")
#app.add_url_rule("/tietokanta/nollaaPelaajanTiedot/<int:pelaajanID>", endpoint="PelaajanTiedot")
#app.add_url_rule("/tietokanta/paivitaPelaajanTiedot/<int:pelaajanID>,<paivitettavaTieto>,<tiedonArvo>", endpoint="PelaajanTiedot")

@app.route("/PelaajanTiedot/hae/")
def hae():
    args = request.args
    vastaus = haePelaajanTiedot(args.get("pelaajanID"))
    return vastaus

@app.route("/PelaajanTiedot/nollaa/")
def nollaa():
    args = request.args
    nollaaPelaajanTiedot(args.get("pelaajanID"))
    return f"pelaajan {args.get("pelaajanID")} tiedot päivitetty"

@app.route("/PelaajanTiedot/paivita/")
def paivita():
    args = request.args
    print(args)
    paivitaPelaajanTiedot(args.get("pelaajanID"), args.get("paivitettavaTieto"), args.get("tiedonArvo"))
    return f"Pelaajan {args.get("pelaajanID")} tieto {args.get("paivitettavaTieto")} muutettu {args.get("tiedonArvo")}"

def funcPaivitaPelaajanTiedot(pelaajanID, paivitettavaTieto, tiedonArvo):
    paivitaPelaajanTiedot(pelaajanID, paivitettavaTieto, tiedonArvo)

def funcNollaaPelaajanTiedot(pelaajanID):
    nollaaPelaajanTiedot(pelaajanID)
    return f"Pelaajan {pelaajanID} tiedot nollattu"

if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)