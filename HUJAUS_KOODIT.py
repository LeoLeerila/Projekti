import asyncio
from tietokanta import Tietokanta

tietokanta = Tietokanta()

async def main():
    await tietokanta.paivitaPelaajanTiedot(17, "co2_budget", 10000)

asyncio.run(main())
