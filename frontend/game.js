const PALVELIN_OSOITE = "http://127.0.0.1:3000";

let pelaajanID;
let pelaajanTiedot;
let kartta, merkkiLahto, merkkiKohde, lentoViiva;
let valittuKohde, lentoTiedot, viimeksiValittuIcao;

const TEHTAVA_PISTE_KERROIN = 2; // Okeasta vastauksesta co2-budjetin lisä pisteet lasketaan kaavalla: lennon co2 kulutus * TEHTAVA_PISTE_KERROIN

// Jonojärjestelmä varmistaa, että vain yksi tehtävä suoritetaan kerrallaan, jottei backend ruuhkaannu.
let onVarattu = false;
const pyyntoJono = [];

// Lisätään pyyntö jonoon prosessoitavaksi
function lisaaJonoon(fn) {
    pyyntoJono.push(fn);
    kasitteleJono();
}

// Prosessoidaan jonon pyyntöjä
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

// Sivun latauduttua lisätään varmuuden vuoksi koko roska jonoon.
window.onload = () => {
    lisaaJonoon(async () => {
        pelaajanID = new URLSearchParams(window.location.search).get("user");
        if (!pelaajanID) {
            // Jos url parametria "user" ei ole ohjataan käyttäjä kirjautumaan.
            window.location.href = "authentication.html";
            return;
        }

        try {
            // Aloitetaan peli logiikka
            pelaajanTiedot = await haePelaajanTiedot();
            await paivitaTilastot();
            luoKartta();
            // Aloitetaan lentotietokone eli lentokentän valinta prosessi.
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

    //console.log(json)
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
    el("stat-co2-budget").textContent = `> CO2-budjetti: ${pelaajanTiedot.co2_budget - pelaajanTiedot.co2_consumed} kg CO₂`;
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
    <b>Lento kohteeseen ${tiedot.lentokentta.name} [${tiedot.lentokentta.country_name}]</b><br>
    Matka: ${tiedot.matkanpituus.toFixed(1)} km<br>
    Aika: ${tiedot.kesto.toFixed(1)} h<br>
    CO₂-kulutus: ${tiedot.co2Lennolta.toFixed(1)} kg CO₂<br>
    Oikean vastauksen pisteet: +${(tiedot.co2Lennolta * TEHTAVA_PISTE_KERROIN).toFixed(1)} kg CO₂
  `).openPopup();

    lentoViiva = L.polyline([lahto, kohde], {
        color: '#00ff00',
        weight: 2,
        dashArray: "5, 10",
        opacity: 0.7
    }).addTo(kartta);

    kartta.fitBounds(L.latLngBounds([lahto, kohde]), { padding: [150, 150] });
}

async function haeLentokenttaVaihtoehdot() {
    /*
    Lentokentta lisan itemi:
        {
            "lentokentan_nimi": lentokentan_tiedot[0],
            "co2Lennolta": data["co2Lennolta"],
            "icao": data['lentokentta'],
            "maa": haePelaajanNykyinenMaa(data['lentokentta'])
        } 
     */
    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/vaihtoehdot/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Lentokenttien haku epäonnistui.");
    const { lentokenttaLista } = await res.json();

    // Jos lentokenttä lista on tyhjä tarkoittaa se pelin häviötä sillä co2 budjetti ei riitä lentämiseen.
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
    // Sortataan lentokentät co2 kulutuksenmukaan niin että lentotietokoneessa lentokentät näkyvät vähiten kuluttavat matkat ensin.
    //console.log(lentokenttaLista)
    lentokenttaLista.sort((a, b) => a.co2Lennolta - b.co2Lennolta);
    //console.log(lentokenttaLista)
    lentokenttaLista.forEach(kentta => {
        const nappi = document.createElement('button');
        nappi.className = "confirm-button";
        nappi.textContent = kentta.lentokentan_nimi + ` [${kentta.maa}]`;
        // Seuraavaksi käsittelemme käyttäjän valinnan
        nappi.onclick = () => lisaaJonoon(async () => await kasitteleValinta(kentta));
        vaihtoehdot.appendChild(nappi);
    });
}

async function kasitteleValinta(kentta) {
    const uusiIcao = kentta.icao;

    // Jos lentokenttää on klikattu kaksi kertaa lentotietokoneessa lennämme kohteeseen. Ensimmäisellä klikkauksella vain kartta päivittyy.
    if (viimeksiValittuIcao === uusiIcao) {
        // Lento on nyt vahvistettu (käyttäjä klikkasi kaksikertaa lentökenttää lentitietokone valikossa) , joten lennämme kohdemaahan.
        await vahvistaLento(kentta);
        viimeksiValittuIcao = null;
        document.getElementById("flight-destination").textContent = "LENTO SUORITETTU.";
        return;
    }

    // Jos päädymme tänne se tarkoittaa, että käyttäjä on klikannut ensimmäisen kerran kyseisestä lentokentästä lentotietokoneen valikossa.
    viimeksiValittuIcao = valittuKohde = uusiIcao;

    // Haetaan lennon koordinaatit, jotta voimme piirtää viivan kartalle lähtöpaikasta määränpäähän. 
    // Huomaa, että paivitaPelaaja=0 tarkoittaa sitä, että emme lennä oikeasti kohteeseen vaan kysymme palvelimelta vain lennon tiedot (pituuden, co2 kulutus, etc.).
    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${valittuKohde}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=0`);
    lentoTiedot = await res.json();
    console.log(lentoTiedot)

    // Piirretään viivat ja annetan lentodataa popuppia varten
    piirraLento(lentoTiedot.koordinaatit.lahto, lentoTiedot.koordinaatit.maaranpaa, Object.assign({}, lentoTiedot, {lentokentta: await haeLentokentanTiedot(lentoTiedot.lentokentta_icao)}));
    document.getElementById("flight-destination").textContent = `VALINTA: ${kentta.lentokentan_nimi} (klikkaa uudelleen vahvistaaksesi)`;
}

async function vahvistaLento(kentta) {
    // Nyt haluamme oikeasti lentää kohteeseen eli haluamme päivittää mm. lennon kulutuksen ja kohteen lentokentän tiedot tietokantaan.
    await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${kentta.icao}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=1`);
    pelaajanTiedot = await haePelaajanTiedot();
    // Tämä päivittää PELAAJAN TIEDOT -elemintin uusilla tiedoille lennettyämme uuteen kenttään.
    await paivitaTilastot();
    document.getElementById("flight-destination").textContent = "LENTO SUORITETTU.";

    // Lennettyämme uuteen maahan tarkistamme, että sijaitseeko lentökenttä Thaimaassa, jos sijaitsee niin pelaaja voittaa.
    const lentokentanTiedot = await haeLentokentanTiedot(kentta.icao)
    if (lentokentanTiedot.country_name === "Thailand") {
        voitto();
        return
    } else if (pelaajanTiedot.co2_consumed >= pelaajanTiedot.co2_budget) {
        // Varmuuden vuoksi tarkistamme myös ettei pelaaja ole ylittänyt co2 budjettia.
        // Tämän pitäisi olla mahdotonta tässä kohtaa, sillä peli logiikan ei anna pelaajan ylittää co2 budjettia koskaan, mutta jos niin sattuu käymään niin tämä estää sen.
        havio();
    }

    // Nyt olemme lentäneet toiseen maahan, eikä maa ole Thaimaa, joten kysymme pelaajalta uuden kysymyksen.
    await naytaKysymys(kentta);
}

async function naytaKysymys(kentta) {
    // Haetaan palvelimelta satunnainen kysymys.
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

    // Käydään läpi kysymyksen mahdolliset vastaukset ja tehdään nappi elementit ja kuunnellaan milloin pelaaja painaa nappia.
    data.mahdollisetVastaukset.forEach(vastaus => {
        const nappi = document.createElement('button');
        nappi.className = "confirm-button";
        nappi.textContent = vastaus;

        // Pelaaja painaa valikosta vastausta. Lisätään varmuuden vuoksi tarkistaVastaus funktio jonojärjestelmäämme.
        nappi.onclick = () => lisaaJonoon(async () => await tarkistaVastaus(vastaus, data.oikeaVastaus, kentta));
        container.appendChild(nappi);
    });
}

async function tarkistaVastaus(valittu, oikea, kentta) {
    const viesti = document.getElementById("flight-destination");

    if (valittu === oikea) {
        // Pelaajan vastaus oli oikea haetaan pelaajan viimeisimmät tiedot ja lisätään co2 budjettin 75.
        pelaajanTiedot = await haePelaajanTiedot();
        const oikeanVastauksenPisteet = kentta.co2Lennolta * TEHTAVA_PISTE_KERROIN
        const uusiBudjetti = pelaajanTiedot.co2_budget + oikeanVastauksenPisteet;

        //console.log(pelaajanTiedot)
        // Päivitetään vielä palvelimen tietokantaan pelaajan uusi co2 budjetti.
        await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/paivita/?pelaajanID=${pelaajanID}&paivitettavaTieto=co2_budget&tiedonArvo=${uusiBudjetti}`);
        viesti.textContent = `Oikea vastaus! Saat +${oikeanVastauksenPisteet.toFixed()} kg CO₂ budjettia.`;
        await paivitaTilastot();
        //console.log(pelaajanTiedot)
    } else {
        viesti.textContent = "Väärä vastaus. Yritä uudelleen seuraavassa kohteessa.";
    }

    //pelaajanTiedot = await haePelaajanTiedot();
    
    await haeLentokenttaVaihtoehdot();
}

function havio() {
    // Tämä hoitaa häviö tekstien tulostamisen lentotietokoneeseen.
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
    // Tämä hoitaa voitto tekstien tulostamisen lentotietokoneeseen.
    const kysymys = document.getElementById('terminal-question');
    kysymys.innerHTML = "";
    const kysymysEl = document.createElement("div");
    kysymysEl.textContent = `> THAIMAA SAAVUTETTU. TEHTÄVÄ SUORITETTU.`;
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
        - Joku äijä 80-luvulla
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
    // Nollataan käyttäjän tiedot palvelimelta eli aloitettaan peli uudestaan.
    const res = await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/nollaa/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Pelaajan tietojen nollaus epäonnistui.");
    return;
}

async function aloitaPeliUudestaan() {
    // Aloitetaan peli uudestaan ja resetetaan pelaajan tiedot palvelimelta ja käyttöliittymästä.
    await nollaaPelaajanTiedot()
    document.getElementById('chat-log').innerHTML = "";
    await paivitaTilastot();
    await haeLentokenttaVaihtoehdot();
}



function vaimo() {
    // Vaimon viestien printtaus
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
    // Kirjauduttuessa ulos pelaaja ohjataan vain kirjautumis sivulle.
    window.location.href = "authentication.html";
}

async function poistaPelaaja() {
    // Postaa pelaajan kannasta kokonaan.
    await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/poista/?pelaajanID=${pelaajanID}`);
    kirjauduUlos();
}

function getRandomInt(min, max) {
    const minCeiled = Math.ceil(min);
    const maxFloored = Math.floor(max);
    return Math.floor(Math.random() * (maxFloored - minCeiled) + minCeiled); // The maximum is exclusive and the minimum is inclusive
  }
  