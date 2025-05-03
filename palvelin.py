from flask import Flask, request, jsonify
from flask_cors import CORS

from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot, paivitaPelaajanTiedot, haeKaikkiPelaajat, lisaaUusiPelaaja
from lopetus import voitto, havio
from kayttoliittyma import palvelinSeuraavaLentokentta
from PeliTehtavat import kysymys
from lentokone import lenna

app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

#Tietokannan funktiot
@app.route("/Pelaajat/kaikki/")
def kaikki_pelaajat():
    """
    Palauttaa JSON-listan kaikista olemassa olevista pelaajista.
    """
    return jsonify(haeKaikkiPelaajat())

@app.route("/Pelaajat/uusi/")
def uusi_pelaaja():
    """
    Luo uusi pelaajaprofiili annetulla nimellä (nimi-parametri).
    Esim: /Pelaajat/uusi/?nimi=Testi
    """
    args = request.args
    nimi = args.get("nimi")
    if not nimi:
        return "Nimi puuttuu", 400

    try:
        uusi_id = lisaaUusiPelaaja(nimi)
        return jsonify({"status": "OK", "id": uusi_id, "nimi": nimi})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    
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

#lentokentät
@app.route("/Lentokentta/vaihtoehdot/")#http://127.0.0.1:3000/Lentokentta/vaihtoehdot/?pelaajanID=1
def vaihtoehdot():
    args = request.args
    vastaus = palvelinSeuraavaLentokentta(args.get("pelaajanID"))
    return vastaus

@app.route("/Lentokentta/uusi/")#http://127.0.0.1:3000/Lentokentta/uusi/?pelaajanID=1&uusiLentokentta=ICAO&nykySijainti=ICAO&paivitaPelaaja=1
def uusi():
    args = request.args
    vastaus = lenna(args.get("uusiLentokentta"), args.get("nykySijainti"), args.get("paivitaPelaaja"), args.get("pelaajanID"))
    return vastaus

if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)