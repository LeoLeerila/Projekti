import mysql.connector

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='flight_game_projekti',
    user='pelaaja',
    password='pelaajansalasana',
    autocommit=True
)

def haePelaajanTiedot(pelaajanId):
    #haetut pelaajan arvot ovat järjestykseesä
    #id, co2_consumed, co2_budget, location, screen_name, time
    sql = f'SELECT * FROM game WHERE id = "{pelaajanId}"'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

def haeMaanLentokentat(maa):
    sql = f'SELECT name FROM airport WHERE ((type = "small_airport") OR (type = "medium_airport") OR (type = "large_airport")) AND iso_country = "{maa}"'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

def haeLentokentanSijainti(lentokentanIdent):
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = "{lentokentanIdent}"'
    kursori = yhteys.cursor()
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
    kursori = yhteys.cursor()
    kursori.execute(sql)
    pass

#lentokentta = etsiMaanLentokentat("KP")
#print(lentokentta)
#paivitaPelaajanCo2(-160)
#paivitaPelaajanSijainti("EFHK")
print(haeLentokentanSijainti("EFHK"))
