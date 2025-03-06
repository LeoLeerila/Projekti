from geopy import distance
from tietokanta import paivitaPelaajanTiedot, haeLentokentanTiedot, haeMaanTiedot

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
        paivitaPelaajanTiedot(pelaajanID, "location", maaranpaa)
        paivitaPelaajanTiedot(pelaajanID, "co2_consumed", co2Lennolta)
        paivitaPelaajanTiedot(pelaajanID, "km_total", matkanpituus)
        paivitaPelaajanTiedot(pelaajanID, "time", kesto)
    else: 
        #palauttaa sanakirjan matkanpituus, kesto, co2Lennolta
        return {"matkanpituus": matkanpituus, "kesto": kesto, "co2Lennolta": co2Lennolta}
    pass

def laskeLennonPituus(lahtosijainti, maanosa):
    #haetaan lähtösijainnin koordinaatit identistä
    lahtosijainti = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", lahtosijainti)
    #haetaan kaikki maanosan maat
    maat = haeMaanTiedot("iso_country", "continent", maanosa)
    tulos = []

    for maa in maat:
        #lasketaan matkan pituus ja co2 päästöt

        matkanpituus = distance.distance(lahtosijainti, haeLentokentanTiedot("latitude_deg, longitude_deg", "iso_country", maa[0])).km
        kesto = matkanpituus / nopeus
        co2Lennolta = co2 * matkanpituus
        #lisätään maan koodi, matkanpituus ja co2 hinta tulokseen
        tulos.append({
            "maa": maa[0], 
            "matkanpituus": matkanpituus, 
            "co2Lennolta": co2Lennolta
        })

    return tulos