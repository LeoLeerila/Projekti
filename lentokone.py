from geopy import distance
import math
import time
from tietokanta import paivitaPelaajanTiedot, haeLentokentanTiedot, haeMaanTiedot, haePelaajanTiedot, haeMaanLentokentat, haeLentokentat

#lentokoneen nopeus km/h
nopeus = 933
#co_2 päästöt kg
co2 = 0.115

def lenna(maaranpaa, sijainti, paivitaPelaaja, pelaajanID):
    #haetaan sijainnin ja määränpään koordinaatit
    maaranpaaKoordinaatit = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", maaranpaa)
    sijaintiKoordinaatit = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", sijainti)
    #lasketaan matkan pituus ja kuinka kauan siinä kestää
    matkanpituus = distance.distance(maaranpaaKoordinaatit, sijaintiKoordinaatit).km
    kesto = matkanpituus / nopeus
    co2Lennolta = co2 * matkanpituus
    if paivitaPelaaja == 1:
        #päivitetään tietokaanta
        pelaajanTiedot = haePelaajanTiedot(pelaajanID)
        paivitaPelaajanTiedot(pelaajanID, "location", maaranpaa)
        paivitaPelaajanTiedot(pelaajanID, "co2_consumed", (co2Lennolta + pelaajanTiedot["co2_consumed"]))
        paivitaPelaajanTiedot(pelaajanID, "km_total", math.ceil(matkanpituus + pelaajanTiedot["km_total"]))
        paivitaPelaajanTiedot(pelaajanID, "time", math.ceil(kesto + pelaajanTiedot["time"]))
    #palauttaa sanakirjan matkanpituus, kesto, co2Lennolta
    return {"matkanpituus": matkanpituus, "kesto": kesto, "co2Lennolta": co2Lennolta}

def laskeLennonPituus(lahtosijainti, maanosa):
    #haetaan lähtösijainnin koordinaatit identistä
    lahtosijainti = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", lahtosijainti)
    #haetaan kaikki maanosan maat
    lentokentat = haeLentokentat()
    tulos = []
    start = time.process_time()
    for lentokentta in lentokentat:
        #lasketaan matkan pituus ja co2 päästöt
        matkanpituus = distance.distance(lahtosijainti, haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", lentokentta[0])).km
        co2Lennolta = co2 * matkanpituus
        #lisätään maan koodi, matkanpituus ja co2 hinta tulokseen
        tulos.append({
            "lentokentta": lentokentta[0], 
            "matkanpituus": matkanpituus, 
            "co2Lennolta": co2Lennolta
        })
    end = time.process_time()

    print(f"It took {end-start} seconds to calculate the distances to {len(lentokentat)} airports.")

    return tulos