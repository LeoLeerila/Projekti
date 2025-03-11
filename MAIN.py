from tietokanta import haePelaajanTiedot
from aloitus import aloitus
from kayttoliittyma import valitseSeuraavaLentokentta

pelaajanTiedot = haePelaajanTiedot(1)
#id, co2_consumed, co2_budget, location, screen_name, time, km_total

peliKaynnissa = 1

if pelaajanTiedot["km_total"] == 0:
    #pelaajalle annetaan pelin aluksi aloitus.py alkuinfo
    aloitus()
    #jos pelaaja haluaa pelaajalle annetaan tutoriaali lentokoneella lentämisestä ja tehtävistä


while peliKaynnissa == 1:
    #päivitetään pelaajaan tiedot
    pelaajanTiedot = haePelaajanTiedot(1)
    #pelaaja valitsee seuraavan maan johon lentää
    valitseSeuraavaLentokentta(pelaajanTiedot["location"])
    #pelaaja tekee tehtävän

    #jos pelaajan co2_consumed on liian suuri eikä hän voi lentää uuteen maahan peli päättyy
    if pelaajanTiedot["co2_consumed"] >= pelaajanTiedot["co2_budget"]:
        peliKaynnissa = 0
        print("peli päättyi")
    #jos pelaaja pääsee thaimaahan pelaaja voittaa pelin ja peli päättyy