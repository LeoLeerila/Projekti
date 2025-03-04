from geopy import distance
from tietokanta import paivitaPelaajanTiedot, haeLentokentanTiedot

#lentokoneen nopeus km/h
nopeus = 933
#co_2 päästöt
co2 = 8

def lenna(maaranpaa, sijainti, paivitaPelaaja):
    #haetaan sijainnin ja määränpään koordinaatit
    maaranpaaKoordinaatit = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", maaranpaa)
    sijaintiKoordinaatit = haeLentokentanTiedot("latitude_deg, longitude_deg", "ident", sijainti)
    #lasketaan matkan pituus ja kuinka kauan siinä kestää
    matkanpituus = distance.distance(maaranpaaKoordinaatit, sijaintiKoordinaatit).km
    kesto = matkanpituus / nopeus
    co2Lennolta = co2 * kesto
    if paivitaPelaaja == 1:
        #päivitetään tietokaanta
        paivitaPelaajanTiedot(1, "location", maaranpaa)
        paivitaPelaajanTiedot(1, "co2_consumed", co2Lennolta)
    print(f"matkan pituus: {matkanpituus} km, joka kestää: {kesto} tuntia")
    pass

#testaus
#lenna("EFHK", "CKQ8", 0)