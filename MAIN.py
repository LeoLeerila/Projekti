from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot
#from aloitus import aloitus
from lopetus import voitto, havio
from kayttoliittyma import valitseSeuraavaLentokentta
from PeliTehtavat import kysymys

pelaajanTiedot = haePelaajanTiedot(1)
#id, co2_consumed, co2_budget, location, screen_name, time, km_total

peliKaynnissa = 1

#if pelaajanTiedot["km_total"] == 0:
    #pelaajalle annetaan pelin aluksi aloitus.py alkuinfo
    #aloitus()
    #jos pelaaja haluaa pelaajalle annetaan tutoriaali lentokoneella lentämisestä ja tehtävistä


while peliKaynnissa == 1:
    #päivitetään pelaajaan tiedot
    pelaajanTiedot = haePelaajanTiedot(1)
    #pelaaja valitsee seuraavan maan johon lentää
    maa = valitseSeuraavaLentokentta(pelaajanTiedot["location"])
    #jos pelaajan co2_consumed on liian suuri eikä hän voi lentää uuteen maahan peli päättyy
    if pelaajanTiedot["co2_consumed"] >= pelaajanTiedot["co2_budget"] or not maa:
        peliKaynnissa = 0
        print("Hävisit pelin :(")
        havio()
        nollaaPelaajanTiedot(1)
        exit()
    #jos pelaaja pääsee thaimaahan pelaaja voittaa pelin ja peli päättyy
    if maa == "VTBD":
        peliKaynnissa = 0
        print("Voitit pelin!")
        voitto()
        nollaaPelaajanTiedot(1)
        exit()
    #pelaaja tekee tehtävän
    kysymys()
    