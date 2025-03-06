from tietokanta import haePelaajanTiedot

pelaajanTiedot = haePelaajanTiedot(1)
#id, co2_consumed, co2_budget, location, screen_name, time, km_total
pelaajanTiedot = {
    "id": pelaajanTiedot[0],
    "co2_consumed": pelaajanTiedot[1],
    "co2_budget": pelaajanTiedot[2],
    "location": pelaajanTiedot[3],
    "screen_name": pelaajanTiedot[4],
    "time": pelaajanTiedot[5],
    "km_total": pelaajanTiedot[6]
}
