import mysql.connector

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='flight_game_projekti',
    user='pelaaja',
    password='pelaajansalasana',
    autocommit=True
)

def etsiMaanLentokentat(maa):
    sql = f'SELECT name FROM airport WHERE ((type = "small_airport") OR (type = "medium_airport") OR (type = "large_airport")) AND iso_country = "{maa}"'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def paivitaPelaajanSijainti(kentanident):
    sql = f'UPDATE game SET location = "{kentanident}" WHERE id = "1";'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    pass

def paivitaPelaajanCo2(co2):
    sql = f'SELECT co2_consumed FROM game WHERE id = "1";'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()[0][0]
    tulos += co2
    
    sql = f'UPDATE game SET co2_consumed = "{tulos}" WHERE id = "1";'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    
    print(tulos)
    pass

#lentokentta = etsiMaanLentokentat("KP")
#print(lentokentta)
#paivitaPelaajanCo2(-160)
#paivitaPelaajanSijainti("EFHK")