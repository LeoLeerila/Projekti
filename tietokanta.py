import mysql.connector
import geopy
from geopy import distance

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='flight_game_projekti',
    user='pelaaja',
    password='pelaajansalasana',
    autocommit=True
)
kursori = yhteys.cursor()



def haePelaajanTiedot(pelaajanId):
    #haetut pelaajan arvot ovat järjestykseesä
    #id, co2_consumed, co2_budget, location, screen_name, time
    sql = f'SELECT * FROM game WHERE id = "{pelaajanId}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]

    tulos = {
    "id": tulos[0],
    "co2_consumed": tulos[1],
    "co2_budget": tulos[2],
    "location": tulos[3],
    "screen_name": tulos[4],
    "time": tulos[5],
    "km_total": tulos[6]
}
    return tulos

def haePelaajanNykyinenMaa(location):
    #hae pelaajan nykyinen maa lentokentan identin mukaan
    sql = f'SELECT iso_country FROM airport WHERE ident = "{location}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0][0]
    sql = f'SELECT name FROM country WHERE iso_country = "{tulos}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0][0]

    return tulos

def haeMaanTiedot(haettavaTieto, rajausTieto, rajausTiedonArvo):
    #hae maan tiedot
    #mahdollisia haettavaTieto ja rajausTieto arvoja ovat
    #iso_country, name, continent, wikipedia_link, keywords
    if rajausTiedonArvo == "*":
        sql = f'SELECT {haettavaTieto} FROM country'
    else:
        sql = f'SELECT {haettavaTieto} FROM country WHERE {rajausTieto} = "{rajausTiedonArvo}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def haeMaanLentokentat(iso_country):
    #((type = "small_airport") OR (type = "medium_airport") OR (type = "large_airport"))
    sql = f'SELECT ident FROM airport WHERE type = "large_airport" AND iso_country = "{iso_country}"'
    kursori.execute(sql)
    try:
        tulos = kursori.fetchall()[0]
    except:
        return
    return tulos

def haeLentokentat():
    sql = f'SELECT ident FROM airport'
    kursori.execute(sql)
    try:
        tulos = kursori.fetchall()
    except:
        return
    return tulos

def haeLentokentanTiedot(haettavaTieto, rajausTieto, rajausTiedonArvo):
    #hae lentokentan tiedot
    #mahdollisia haettavaTieto ja rajausTieto arvoja ovat
    #id, ident, type, name, latitude_deg, longitude_deg, elevation_ft, continent, iso_country, iso_region, municipality, scheduled_service, gps_code, iata_code, local_code, home_link, wikipedia_link, keywords
    sql = f'SELECT {haettavaTieto} FROM airport WHERE {rajausTieto} = "{rajausTiedonArvo}"'
    kursori.execute(sql)
    try:
        tulos = kursori.fetchall()[0]
    except:
        return
    return tulos

def annakysymys(kysymysRajaus):
    #haetaan kysymyksiä tietokannasta
    #kysymysnumero, kysymys_vaihtoehdot, vastaus_vaihtoehdot, vastaukset
    sql = f'SELECT kysymys_vaihtoehdot FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

def annakysymysVaihtoehto(kysymysRajaus, vaihtoehto):
    sql = f'SELECT vastaus_vaihtoehto{vaihtoehto} FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos
"""
def annakysymysVaihtoehto2(kysymysRajaus):
    sql = f'SELECT vastaus_vaihtoehto2 FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

def annakysymysVaihtoehto3(kysymysRajaus):
    sql = f'SELECT vastaus_vaihtoehto3 FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos
"""
def annavastaus(kysymysRajaus):
    #haetaan vastauksia tietokannasta
    #vastaukset
    sql = f'SELECT vastaukset FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def paivitaPelaajanTiedot(pelaajanId, paivitettavaTieto, tiedonArvo):
    #mahdollisia päivityksiä pelaajan tietoihin ovat
    #id, co2_consumed, co2_budget, location, screen_name, time
    sql = f'UPDATE game SET {paivitettavaTieto} = "{tiedonArvo}" WHERE id = "{pelaajanId}";'
    kursori.execute(sql)
    pass

def nollaaPelaajanTiedot(pelaajanId):
    sql = f'UPDATE game SET co2_consumed = "0", co2_budget = "100", location = "EFHK", screen_name = "PLAYER", time = "0", km_total = "0" WHERE id = "{pelaajanId}";'
    kursori.execute(sql)
    pass

