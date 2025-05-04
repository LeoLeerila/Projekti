from flask import Flask, request, jsonify
from flask_cors import CORS

from tietokanta import Tietokanta
# haePelaajanTiedot, nollaaPelaajanTiedot, paivitaPelaajanTiedot, haeKaikkiPelaajat, lisaaUusiPelaaja, haeLentokentanTiedot, haePelaajanNykyinenMaa, haeMaanTiedot, poistaPelaaja
from kayttoliittyma import palvelinSeuraavaLentokentta
from PeliTehtavat import palvelinKysymys
from lentokone import lenna

app = Flask(__name__)

cors = CORS(app)

tietokanta = Tietokanta()

app.config['CORS_HEADERS'] = 'Content-Type'

#Tietokannan funktiot
@app.route("/Pelaajat/kaikki/")
async def kaikki_pelaajat():
    """
    Palauttaa JSON-listan kaikista olemassa olevista pelaajista.
    """
    return jsonify(await tietokanta.haeKaikkiPelaajat())

@app.route("/Pelaajat/uusi/")
async def uusi_pelaaja():
    """
    Luo uusi pelaajaprofiili annetulla nimellä (nimi-parametri).
    Esim: /Pelaajat/uusi/?nimi=Testi
    """
    args = request.args
    nimi = args.get("nimi")
    if not nimi:
        return "Nimi puuttuu", 400

    try:
        uusi_id = await tietokanta.lisaaUusiPelaaja(nimi)
        return jsonify({"status": "OK", "id": uusi_id, "nimi": nimi})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    
@app.route("/PelaajanTiedot/hae/")#http://127.0.0.1:3000/PelaajanTiedot/hae/?pelaajanID=1
async def hae():
    args = request.args
    vastaus = await tietokanta.haePelaajanTiedot(args.get("pelaajanID"))
    sijainti = await tietokanta.haePelaajanNykyinenMaa(vastaus["location"])

    # | mergaa kaksi sanakirjaa yhteen
    return vastaus | {"country_name":sijainti}

@app.route("/PelaajanTiedot/nollaa/")#http://127.0.0.1:3000/PelaajanTiedot/nollaa/?pelaajanID=1
async def nollaa():
    args = request.args
    await tietokanta.nollaaPelaajanTiedot(args.get("pelaajanID"))
    return [f"pelaajan {args.get("pelaajanID")} tiedot päivitetty"]

@app.route("/PelaajanTiedot/paivita/")#http://127.0.0.1:3000/PelaajanTiedot/paivita/?pelaajanID=1&paivitettavaTieto=co2_consumed&tiedonArvo=100
async def paivita():
    args = request.args
    await tietokanta.paivitaPelaajanTiedot(args.get("pelaajanID"), args.get("paivitettavaTieto"), args.get("tiedonArvo"))
    return [f"Pelaajan {args.get("pelaajanID")} tieto {args.get("paivitettavaTieto")} muutettu {args.get("tiedonArvo")}"]

@app.route("/PelaajanTiedot/poista/")#http://127.0.0.1:3000/PelaajanTiedot/poista/?pelaajanID=1
async def poista():
    args = request.args
    await tietokanta.poistaPelaaja(args.get("pelaajanID"))
    return [f"Pelaaja {args.get("pelaajanID")} on postettu kannasta."]

#lentokentät
@app.route("/Lentokentta/vaihtoehdot/")#http://127.0.0.1:3000/Lentokentta/vaihtoehdot/?pelaajanID=1
async def vaihtoehdot():
    args = request.args
    vastaus = await palvelinSeuraavaLentokentta(args.get("pelaajanID"))
    return vastaus

@app.route("/Lentokentta/uusi/")#http://127.0.0.1:3000/Lentokentta/uusi/?pelaajanID=1&uusiLentokentta=ICAO&nykySijainti=ICAO&paivitaPelaaja=1
async def uusi():
    args = request.args

    vastaus = await lenna(args.get("uusiLentokentta"), args.get("nykySijainti"), int(args.get("paivitaPelaaja")), args.get("pelaajanID"))
    return vastaus

@app.route("/Lentokentta/tiedot/")#http://127.0.0.1:3000/Lentokentta/tiedot/?icao=EFHK
async def tiedot():
    args = request.args
    vastaus = await tietokanta.haeLentokentanTiedot("*", "ident", args.get("icao"))
    sijainti = await tietokanta.haeMaanTiedot("name", "iso_country", vastaus[8])

    json = {
        "id": vastaus[0],
        "ident": vastaus[1],
        "type": vastaus[2],
        "name": vastaus[3],
        "latitude_deg": vastaus[4],
        "longitude_deg": vastaus[5],
        "elevation_ft": vastaus[6],
        "continent": vastaus[7],
        "iso_country": vastaus[8],
        "iso_region": vastaus[9],
        "municipality": vastaus[10],
        "scheduled_service": vastaus[11],
        "gps_code": vastaus[12],
        "iata_code": vastaus[13],
        "local_code": vastaus[14],
        "home_link": vastaus[15],
        "wikipedia_link": vastaus[16],
        "keywords": vastaus[17],
        "country_name": sijainti
    }

    return json

#kysymykset
@app.route("/kysymykset/kysymys/")#http://127.0.0.1:3000/kysymykset/kysymys/
async def kysymys():
    return await palvelinKysymys()



if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)