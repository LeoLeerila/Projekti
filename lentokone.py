from geopy import distance
from tietokanta import paivitaPelaajanSijainti, paivitaPelaajanCo2

#lentokoneen nopeus km/h
nopeus = 933
#co_2 päästöt
co2 = 8

def lenna(maaranpaa, sijainti):
    #lasketaan matkan pituus ja kuinka kauan siinä kestää
    matkanpituus = distance.distance(maaranpaa, sijainti).km
    kesto = matkanpituus / nopeus
    co2Lennolta = co2 * kesto
    #päivitetään tietokaanta
    #paivitaPelaajanSijainti(maaranpaa)
    paivitaPelaajanCo2(co2Lennolta)
    print(f"matkan pituus: {matkanpituus} km, joka kestää: {kesto} tuntia")
    pass

#testaus
#lenna((60.3172,24.963301),(60.6544,24.8811))