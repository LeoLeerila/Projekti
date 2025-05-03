const PALVELIN_OSOITE = "http://127.0.0.1:3000";

let pelaajanID;
let pelaajanTiedot;
let kartta, merkkiLahto, merkkiKohde, lentoViiva;
let valittuKohde, lentoTiedot, viimeksiValittuIcao;

// Jonojärjestelmä varmistaa, että vain yksi tehtävä suoritetaan kerrallaan, jottei backend ruuhkaannu.
let onVarattu = false;
const pyyntoJono = [];

function lisaaJonoon(fn) {
    pyyntoJono.push(fn);
    kasitteleJono();
}

async function kasitteleJono() {
    if (onVarattu || pyyntoJono.length === 0) return;
    onVarattu = true;
    const tehtava = pyyntoJono.shift();
    try {
        await tehtava();
    } catch (virhe) {
        console.error("Virhe jonossa:", virhe);
    } finally {
        onVarattu = false;
        kasitteleJono();
    }
}

// Käynnistetään peli sivun latautuessa
window.onload = () => {
    lisaaJonoon(async () => {
        pelaajanID = new URLSearchParams(window.location.search).get("user");
        if (!pelaajanID) {
            window.location.href = "authentication.html";
            return;
        }

        try {
            pelaajanTiedot = await haePelaajanTiedot();
            await paivitaTilastot();
            luoKartta();
            await haeLentokenttaVaihtoehdot();
        } catch (err) {
            alert("Virhe: " + err.message);
        }
    });
};

async function haePelaajanTiedot() {
    const res = await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/hae/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Pelaajan tietojen haku epäonnistui.");
    const json = await res.json()

    console.log(json)
    return json;
}

async function haeLentokentanTiedot(icao) {
    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/tiedot/?icao=${icao}`);
    if (!res.ok) throw new Error("Lentokentän tietojen haku epäonnistui.");
    return res.json();
}

async function paivitaTilastot() {
    pelaajanTiedot = await haePelaajanTiedot();
    const el = (id) => document.getElementById(id);
    el("stat-name").textContent = `> Nimi: ${pelaajanTiedot.screen_name}`;
    el("stat-location").textContent = `> Sijainti: ${pelaajanTiedot.location_name}`;
    el("stat-co2-budget").textContent = `> CO2 budjetti: ${pelaajanTiedot.co2_budget - pelaajanTiedot.co2_consumed}`;
    el("stat-distance").textContent = `> Lennetty matka: ${pelaajanTiedot.km_total} km`;
    el("stat-time").textContent = `> Lentoaika: ${pelaajanTiedot.time} h`;
}

function luoKartta() {
    kartta = L.map("world-map").setView([20, 0], 2);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        zoomControl: false
    }).addTo(kartta);
}

function merkinTyyli() {
    return {
        radius: 6,
        color: '#00ff00',
        fillColor: '#00ff00',
        fillOpacity: 0.8
    };
}

function piirraLento(lahto, kohde, tiedot) {
    [merkkiLahto, merkkiKohde, lentoViiva].forEach(layer => layer && kartta.removeLayer(layer));

    merkkiLahto = L.circleMarker(lahto, merkinTyyli()).addTo(kartta).bindPopup("Lähtö");
    merkkiKohde = L.circleMarker(kohde, merkinTyyli()).addTo(kartta).bindPopup(`
    <b>Lento</b><br>
    Matka: ${tiedot.matkanpituus.toFixed(1)} km<br>
    Aika: ${tiedot.kesto.toFixed(1)} h<br>
    CO₂-kulutus: ${tiedot.co2Lennolta.toFixed(1)} kg
  `).openPopup();

    lentoViiva = L.polyline([lahto, kohde], {
        color: '#00ff00',
        weight: 2,
        dashArray: "5, 10",
        opacity: 0.7
    }).addTo(kartta);

    kartta.fitBounds(L.latLngBounds([lahto, kohde]), { padding: [80, 80] });
}

async function haeLentokenttaVaihtoehdot() {
    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/vaihtoehdot/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Lentokenttien haku epäonnistui.");
    const { lentokenttaLista } = await res.json();

    if (lentokenttaLista.length === 0) {
        havio();
        return
    } else if (pelaajanTiedot.country_name === "Thailand") {
        voitto();
        return
    }

    const kysymys = document.getElementById('terminal-question');
    kysymys.innerHTML = "";
    const kysymysEl = document.createElement("div");
    kysymysEl.textContent = "> Mihin haluaisit lentää seuraavaksi?";
    kysymysEl.className = "terminal-input";
    kysymys.appendChild(kysymysEl);

    const vaihtoehdot = document.getElementById('flight-options');
    vaihtoehdot.innerHTML = "";
    lentokenttaLista.sort((a, b) => a.co2Lennolta - b.co2Lennolta);
    lentokenttaLista.forEach(kentta => {
        const nappi = document.createElement('button');
        nappi.className = "confirm-button";
        nappi.textContent = kentta.lentokentan_nimi + ` [${kentta.maa}]`;
        nappi.onclick = () => lisaaJonoon(() => kasitteleValinta(kentta));
        vaihtoehdot.appendChild(nappi);
    });
}

async function kasitteleValinta(kentta) {
    const uusiIcao = kentta.icao;

    if (viimeksiValittuIcao === uusiIcao) {
        await vahvistaLento();
        viimeksiValittuIcao = null;
        document.getElementById("flight-destination").textContent = "LENTO SUORITETTU.";
        return;
    }

    viimeksiValittuIcao = valittuKohde = uusiIcao;

    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${valittuKohde}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=0`);
    lentoTiedot = await res.json();

    piirraLento(lentoTiedot.koordinaatit.lahto, lentoTiedot.koordinaatit.maaranpaa, lentoTiedot);
    document.getElementById("flight-destination").textContent = `VALINTA: ${kentta.lentokentan_nimi} (klikkaa uudelleen vahvistaaksesi)`;
}

async function vahvistaLento() {
    await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${valittuKohde}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=1`);
    pelaajanTiedot = await haePelaajanTiedot();
    await paivitaTilastot();
    document.getElementById("flight-destination").textContent = "LENTO SUORITETTU.";

    const lentokentanTiedot = await haeLentokentanTiedot(valittuKohde)

    if (lentokentanTiedot.country_name === "Thailand") {
        voitto();
    } else if (pelaajanTiedot.co2_consumed >= pelaajanTiedot.co2_budget) {
        havio();
    }

    await naytaKysymys();
}

async function naytaKysymys() {
    const res = await fetch(`${PALVELIN_OSOITE}/kysymykset/kysymys/`);
    const data = await res.json();

    const container = document.getElementById("flight-options");
    container.innerHTML = "";

    const kysymys = document.getElementById('terminal-question');
    kysymys.innerHTML = "";
    const kysymysEl = document.createElement("div");
    kysymysEl.textContent = `> ${data.kysymys}`;
    kysymysEl.className = "terminal-input";
    kysymys.appendChild(kysymysEl);

    data.mahdollisetVastaukset.forEach(vastaus => {
        const nappi = document.createElement('button');
        nappi.className = "confirm-button";
        nappi.textContent = vastaus;
        nappi.onclick = () => lisaaJonoon(() => tarkistaVastaus(vastaus, data.oikeaVastaus));
        container.appendChild(nappi);
    });
}

async function tarkistaVastaus(valittu, oikea) {
    const viesti = document.getElementById("flight-destination");

    if (valittu === oikea) {
        pelaajanTiedot = await haePelaajanTiedot();
        const uusiBudjetti = pelaajanTiedot.co2_budget + 75;
        await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/paivita/?pelaajanID=${pelaajanID}&paivitettavaTieto=co2_budget&tiedonArvo=${uusiBudjetti}`);
        viesti.textContent = "Oikea vastaus! Saat +75 kg CO₂ budjettia.";
    } else {
        viesti.textContent = "Väärä vastaus. Yritä uudelleen seuraavassa kohteessa.";
    }

    pelaajanTiedot = await haePelaajanTiedot();
    await paivitaTilastot();
    await haeLentokenttaVaihtoehdot();
}

function havio() {
    const kysymys = document.getElementById('terminal-question');
    kysymys.innerHTML = "";
    const kysymysEl = document.createElement("div");
    kysymysEl.textContent = `> SYSTEM ERROR [0xCO2FATAL]`;
    kysymysEl.className = "terminal-input";
    kysymys.appendChild(kysymysEl);

    const container = document.getElementById("flight-options");
    container.innerHTML = "";
    const gameLost = document.createElement('pre')
    gameLost.innerHTML = `
        CO₂-budjetti ylitetty.
        Planeetta huokaisi syvään.

        🔌 Sammutetaan lentokonetta...
        💸 Päästölasku: lähetetty verottajalle.
        ☁️ Ilmasto lämpenee... sinusta riippumatta.

        "Paska reissu, mutta tulipahan tehtyä."
        - ${pelaajanTiedot.screen_name}
    `
    container.appendChild(gameLost)

    const nappi = document.createElement('button');
    nappi.className = "confirm-button";
    nappi.textContent = "Aloita peli uudestaan";
    nappi.style.textAlign = "center"
    nappi.onclick = () => aloitaPeliUudestaan();

    container.appendChild(nappi);
}

function voitto() {
    const kysymys = document.getElementById('terminal-question');
    kysymys.innerHTML = "";
    const kysymysEl = document.createElement("div");
    kysymysEl.textContent = `> BANGKOK SAAVUTETTU. TEHTÄVÄ SUORITETTU.`;
    kysymysEl.className = "terminal-input";
    kysymys.appendChild(kysymysEl);

    const container = document.getElementById("flight-options");
    container.innerHTML = "";
    const gameLost = document.createElement('pre')
    gameLost.innerHTML = `
        🛏️ Riippumatto otettu käyttöön...
        🥥 Kookosjuoma pyöräytetty...
        📉 CO₂ vaihdettu Finnairin pluspisteisiin...

        🧳 Työmatka selvästi raskas. Olo kevenee.
        📵 Vaimolle ei vielä soiteta. Ei tarvitse huolestuttaa.

        "One night in Bangkok and the world's your oyster."
        - Some guy in the 80s
    `

    container.appendChild(gameLost)

    const nappi = document.createElement('button');
    nappi.className = "confirm-button";
    nappi.textContent = "Aloita peli uudestaan";
    nappi.style.textAlign = "center"
    nappi.onclick = () => aloitaPeliUudestaan();

    container.appendChild(nappi);
}

async function nollaaPelaajanTiedot() {
    const res = await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/nollaa/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Pelaajan tietojen nollaus epäonnistui.");
    return;
}

async function aloitaPeliUudestaan() {
    await nollaaPelaajanTiedot()

    await paivitaTilastot();
    await haeLentokenttaVaihtoehdot();
}



function vaimo() {
    const chatLog = document.getElementById('chat-log')

    let index = 0;
    const maxMessages = greetings.length;
    setInterval(() => {
        if (index >= maxMessages) {
            index = 0;
            return;
        }
        const viesti = document.createElement("div");
        viesti.className = "chat-message";
        viesti.textContent = `> ${greetings[index]}`;
        chatLog.appendChild(viesti);
        chatLog.scrollTop = chatLog.scrollHeight;
        index++;
    }, getRandomInt(1000, 10000))
}

vaimo()

function kirjauduUlos() {
    window.location.href = "authentication.html";
}

function getRandomInt(min, max) {
    const minCeiled = Math.ceil(min);
    const maxFloored = Math.floor(max);
    return Math.floor(Math.random() * (maxFloored - minCeiled) + minCeiled); // The maximum is exclusive and the minimum is inclusive
  }
  