from tietokanta import haePelaajanTiedot

pelaajanTiedot = []
for tieto in haePelaajanTiedot(1):
    pelaajanTiedot.append(tieto)
#pelaajan tiedot ovat järjestyksessä
#id, co2_consumed, co2_budget, location, screen_name, time

