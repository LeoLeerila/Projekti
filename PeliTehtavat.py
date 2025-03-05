import mysql.connector

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='flight_game_projekti',
    user='pelaaja',
    password='pelaajansalasana',
    autocommit=True
)
kursori = yhteys.cursor()
def annakysymys():
    sql = f'SELECT * FROM tehtavat WHERE kysymysnumero = "{1}"'
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos