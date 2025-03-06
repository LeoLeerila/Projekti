from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot
from kayttoliittyma import valitseSeuraavaLentokentta, testiTehtava
import os
import time

win_frames = [
    r"""
     \O/  
      |   
     / \  
    """,
    r"""
      O   
     /|\  
     / \  
    """,
    r"""
     /O\  
      |   
     / \  
    """,
    r"""
      O/  
     /|   
     / \  
    """
]

loss_frames = [
    r"""
      _______  _______  _______ 
     (  ____ \(  ___  )(  ____ \
     | (    \/| (   ) || (    \/
     | (_____ | |   | || (_____ 
     (_____  )| |   | |(_____  )
           ) || |   | |      ) |
     /\____) || (___) |/\____) |
     \_______)(_______)\_______)
    
            GAME OVER
    """,
    r"""
      ____   ___  ____  
     / ___) / __)(  _ \ 
     \___ \( (__  )   / 
     (____/ \___)(__\_)
    
            GAME OVER
    """
]

pelaajanTiedot = haePelaajanTiedot(1)
#id, co2_consumed, co2_budget, location, screen_name, time, km_total

peliKaynnissa = 1

if pelaajanTiedot["km_total"] == 0:
    #pelaajalle annetaan pelin aluksi aloitus.py alkuinfo
    from aloitus import aloitus
    #jos pelaaja haluaa pelaajalle annetaan tutoriaali lentokoneella lentämisestä ja tehtävistä


while peliKaynnissa == 1:
    #pelaaja valitsee seuraavan maan johon lentää
    pelaajanTiedot = haePelaajanTiedot(1)
    maa = valitseSeuraavaLentokentta(pelaajanTiedot["location"])
    #print(maa)

    #jos pelaajan co2_consumed on liian suuri eikä hän voi lentää uuteen maahan peli päättyy
    if pelaajanTiedot["co2_consumed"] >= pelaajanTiedot["co2_budget"] or not maa:
        peliKaynnissa = 0
        print("Hävisit pelin :(")
        nollaaPelaajanTiedot(1)
        exit()
    #jos pelaaja pääsee thaimaahan pelaaja voittaa pelin ja peli päättyy
    if maa == "VTBD":
        print("Voitit pelin!")
        peliKaynnissa = 0
        nollaaPelaajanTiedot(1)
        exit()

    if maa:
        testiTehtava()