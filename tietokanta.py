import mysql.connector
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
    return tulos

def haeMaanTiedot(haettavaTieto, rajausTieto, rajausTiedonArvo):
    #hae maan tiedot
    #mahdollisia haettavaTieto ja rajausTieto arvoja ovat
    #iso_country, name, continent, wikipedia_link, keywords
    sql = f'SELECT {haettavaTieto} FROM country WHERE {rajausTieto} = "{rajausTiedonArvo}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def haeMaanLentokentat(iso_country):
    #((type = "small_airport") OR (type = "medium_airport") OR (type = "large_airport"))
    sql = f'SELECT ident FROM airport WHERE type = "large_airport" AND iso_country = "{iso_country}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

def haeLentokentanTiedot(haettavaTieto, rajausTieto, rajausTiedonArvo):
    #hae lentokentan tiedot
    #mahdollisia haettavaTieto ja rajausTieto arvoja ovat
    #id, ident, type, name, latitude_deg, longitude_deg, elevation_ft, continent, iso_country, iso_region, municipality, scheduled_service, gps_code, iata_code, local_code, home_link, wikipedia_link, keywords
    sql = f'SELECT {haettavaTieto} FROM airport WHERE {rajausTieto} = "{rajausTiedonArvo}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

'''def paivitaPelaajanSijainti(pelaajanId, kentanIdent):
    sql = f'UPDATE game SET location = "{kentanIdent}" WHERE id = "{pelaajanId}";'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    pass'''

def paivitaPelaajanTiedot(pelaajanId, paivitettavaTieto, tiedonArvo):
    #mahdollisia päivityksiä pelaajan tietoihin ovat
    #id, co2_consumed, co2_budget, location, screen_name, time
    sql = f'UPDATE game SET {paivitettavaTieto} = "{tiedonArvo}" WHERE id = "{pelaajanId}";'
    kursori.execute(sql)
    pass

def laskeLennonPituus(lahtosijainti, maanosa):
    #haetaan kaikki maanosan maat
    maat = haeMaanTiedot("iso_country", "continent", maanosa)
    tulos = []

    for maa in maat:
        #lasketaan matkan pituus ja co2 päästöt
        matkanpituus = distance.distance(lahtosijainti, haeLentokentanTiedot("latitude_deg, longitude_deg", "iso_country", maa[0])).km
        kesto = matkanpituus / 933
        co2Lennolta = 8 * kesto
        #lisätään maan koodi, matkanpituus ja co2 hinta tulokseen
        tulos.append([maa[0], matkanpituus, co2Lennolta])

    return tulos


#print(haePelaajanTiedot(1))
#print(haeMaanTiedot("name", "iso_country", "FI"))
#print(haeMaanLentokentat("US"))
#print(haeLentokentanTiedot("name, type, municipality", "ident", "EFHK"))
#print(haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", "EFHK"))
'''for asda in laskeLennonPituus((53.2400016784668, 50.375), "EU"):
    asa = haeMaanTiedot("name", "iso_country", asda[0])[0][0]
    print(asda)
    print(asa)'''