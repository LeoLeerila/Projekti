from geopy import distance

#lentokoneen nopeus km/h
nopeus = 250
#co_2 päästöt
co2 = 1

def lenna(maaranpaa, sijainti):
    #lasketaan matkan pituus ja kuinka kauan siinä kestää
    matkanpituus = distance.distance(maaranpaa, sijainti).km
    kesto = matkanpituus / nopeus
    #päivitetään tietokaanta

    print(f"matkan pituus: {matkanpituus} km, joka kestää: {kesto} tuntia")
    pass

#testaus
#lenna((60.3172,24.963301),(60.6544,24.8811))