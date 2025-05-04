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
kursori = yhteys.cursor(buffered=True)

class Tietokanta:

    async def haeKaikkiPelaajat(self):
        """
        Hakee kaikki pelaajaprofiilit tietokannasta.
        Palauttaa listan sanakirjoja, joissa on pelaajan ID ja nimi.
        """
        sql = "SELECT id, screen_name FROM game ORDER BY id ASC"
        kursori.execute(sql)
        return [{"id": r[0], "screen_name": r[1]} for r in kursori.fetchall()]

    async def lisaaUusiPelaaja(self,nimi):
        """
        Lisää uusi pelaaja 'game'-tauluun oletusarvoilla.
        Palauttaa uuden pelaajan ID:n.
        """
        # Tarkistetaan onko nimi jo käytössä (valinnainen lisäominaisuus)
        sql_check = "SELECT COUNT(*) FROM game WHERE screen_name = %s"
        kursori.execute(sql_check, (nimi,))
        if kursori.fetchone()[0] > 0:
            raise Exception("Nimi on jo olemassa.")

        # Lisätään uusi pelaaja
        sql = """
        INSERT INTO game (co2_consumed, co2_budget, location, screen_name, time, km_total)
        VALUES (0, 100, 'EFHK', %s, 0, 0)
        """
        kursori.execute(sql, (nimi,))
        return kursori.lastrowid

    async def poistaPelaaja(self,pelaajanId):
        """
        Poistaa pelaajan tietokannasta annetulla pelaajan ID:llä.
        """
        sql = "DELETE FROM game WHERE id = %s"
        kursori.execute(sql, (pelaajanId,))


    async def haePelaajanTiedot(self,pelaajanId):
        #haetut pelaajan arvot ovat järjestykseesä
        #id, co2_consumed, co2_budget, location, screen_name, time
        sql = f'SELECT game.*, airport.name FROM game LEFT JOIN airport ON game.location = airport.ident WHERE game.id = "{pelaajanId}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0]

        tulos = {
        "id": tulos[0],
        "co2_consumed": tulos[1],
        "co2_budget": tulos[2],
        "location": tulos[3],
        "screen_name": tulos[4],
        "time": tulos[5],
        "km_total": tulos[6],
        "location_name": tulos[7]
        }
        return tulos

    async def haePelaajanNykyinenMaa(self,location):
        sql = f'SELECT country.name FROM airport LEFT JOIN country ON airport.iso_country = country.iso_country WHERE airport.ident = "{location}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0][0]
        #hae pelaajan nykyinen maa lentokentan identin mukaan
        """
        sql = f'SELECT iso_country FROM airport WHERE ident = "{location}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0][0]
        sql = f'SELECT name FROM country WHERE iso_country = "{tulos}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0][0]
        """
        return tulos

    async def haeMaanTiedot(self,haettavaTieto, rajausTieto, rajausTiedonArvo):
        #hae maan tiedot
        #mahdollisia haettavaTieto ja rajausTieto arvoja ovat
        #iso_country, name, continent, wikipedia_link, keywords
        if rajausTiedonArvo == "*":
            sql = f'SELECT {haettavaTieto} FROM country'
        else:
            sql = f'SELECT {haettavaTieto} FROM country WHERE {rajausTieto} = "{rajausTiedonArvo}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0][0]
        return tulos

    async def haeMaanLentokentat(self,iso_country):
        #((type = "small_airport") OR (type = "medium_airport") OR (type = "large_airport"))
        sql = f'SELECT ident FROM airport WHERE type = "large_airport" AND iso_country = "{iso_country}"'
        kursori.execute(sql)
        try:
            tulos = kursori.fetchall()[0]
        except:
            return
        return tulos

    async def haeLentokentat(self):
        sql = f'SELECT ident FROM airport WHERE type = "large_airport"'
        kursori.execute(sql)
        try:
            tulos = kursori.fetchall()
        except:
            return
        return tulos

    async def haeLentokentanTiedot(self,haettavaTieto, rajausTieto, rajausTiedonArvo):
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

    async def annakysymys(self,kysymysRajaus):
        #haetaan kysymyksiä tietokannasta
        #kysymysnumero, kysymys_vaihtoehdot, vastaus_vaihtoehdot, vastaukset
        sql = f'SELECT kysymys_vaihtoehdot FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()[0]
        return tulos

    async def annakysymysVaihtoehto(self,kysymysRajaus, vaihtoehto):
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
    async def annavastaus(self,kysymysRajaus):
        #haetaan vastauksia tietokannasta
        #vastaukset
        sql = f'SELECT vastaukset FROM tehtavat WHERE kysymysnumero = "{kysymysRajaus}"'
        kursori.execute(sql)
        tulos = kursori.fetchall()
        return tulos

    async def paivitaPelaajanTiedot(self,pelaajanId, paivitettavaTieto, tiedonArvo):
        #mahdollisia päivityksiä pelaajan tietoihin ovat
        #id, co2_consumed, co2_budget, location, screen_name, time
        sql = f'UPDATE game SET {paivitettavaTieto} = "{tiedonArvo}" WHERE id = "{pelaajanId}";'
        kursori.execute(sql)
        pass

    async def nollaaPelaajanTiedot(self,pelaajanId):
        sql = f'UPDATE game SET co2_consumed = "0", co2_budget = "100", location = "EFHK", time = "0", km_total = "0" WHERE id = "{pelaajanId}";'
        kursori.execute(sql)
        pass

