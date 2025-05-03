const PALVELIN_OSOITE = "http://127.0.0.1:3000";
let pelaajanID = null;
let pelaajanTiedot = null;
let map = null;
let markerA = null;
let markerB = null;
let flightLine = null;
let valittuKohde = null;
let lentodata = null;


// Hakee pelaajan tiedot palvelimelta
async function haePelaajanTiedot() {
    const res = await fetch(`${PALVELIN_OSOITE}/PelaajanTiedot/hae/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Pelaajan tietojen haku epäonnistui.");
    return await res.json();
}

// Päivittää statit HTML-näkymään
function paivitaStatit(tiedot) {
    document.getElementById("stat-co2-consumed").textContent = `> CO2 kulutettu: ${tiedot.co2_consumed}`;
    document.getElementById("stat-co2-budget").textContent = `> CO2 budjetti: ${tiedot.co2_budget}`;
    document.getElementById("stat-distance").textContent = `> Lennetty matka: ${tiedot.km_total} km`;
    document.getElementById("stat-time").textContent = `> Lentoaika: ${tiedot.time} h`;
}

// Suoritetaan sivun latauksen yhteydessä
async function kaynnistaPeli() {
    const params = new URLSearchParams(window.location.search);
    pelaajanID = params.get("user");

    if (!pelaajanID) {
        window.location.href = "authentication.html";
        return;
    }

    try {
        pelaajanTiedot = await haePelaajanTiedot();
        paivitaStatit(pelaajanTiedot);
        luoKartta();
        await haeLentokentat()
    } catch (err) {
        alert("Virhe: " + err.message);
    }
}

function luoKartta() {
    map = L.map("world-map").setView([20, 0], 2);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        maxZoom: 19,
        zoomControl: false
      }).addTo(map);
      
}

function piirraLento(lahto, kohde, lentodata) {
    /**
     * Esimerkki:

        piirraLento([60.3172, 24.9633], [13.9126, 100.6066], {
            matkanpituus: 7924,
            kesto: 8.5,
            co2Lennolta: 911
        });

     * 
     */
    
    // Poista vanhat
    if (markerA) map.removeLayer(markerA);
    if (markerB) map.removeLayer(markerB);
    if (flightLine) map.removeLayer(flightLine);

    markerA = L.circleMarker([lahto[0], lahto[1]], {
        radius: 6,
        color: '#00ff00',
        fillColor: '#00ff00',
        fillOpacity: 0.8
      }).addTo(map).bindPopup("Lähtö");
      
      markerB = L.circleMarker([kohde[0], kohde[1]], {
        radius: 6,
        color: '#00ff00',
        fillColor: '#00ff00',
        fillOpacity: 0.8
      }).addTo(map).bindPopup("Kohde");
      
      flightLine = L.polyline([lahto, kohde], {
        color: '#00ff00',
        weight: 2,
        dashArray: "5, 10",
        opacity: 0.7
      }).addTo(map);
      

    // Näytä info popuppina
    const popup = `
      <b>Lento</b><br>
      Matka: ${lentodata.matkanpituus.toFixed(1)} km<br>
      Aika: ${lentodata.kesto.toFixed(1)} h<br>
      CO₂: ${lentodata.co2Lennolta.toFixed(1)} kg
    `;
    markerB.bindPopup(popup).openPopup();

    // Keskitetään kartta kahden pisteen keskelle
    const bounds = L.latLngBounds([lahto, kohde]);
    map.fitBounds(bounds, { padding: [20, 20] });
}

async function haeLentokentat() {
    const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/vaihtoehdot/?pelaajanID=${pelaajanID}`);
    if (!res.ok) throw new Error("Lentokenttien haku epäonnistui.");

    const lentokentat = await res.json();
    const tietokone = document.getElementById('flight-computer');

    lentokentat.lentokenttaLista.forEach(kentta => {
        const nappi = document.createElement('button');
        nappi.className = "confirm-button";
        nappi.innerText = kentta.lentokentan_nimi;
        nappi.onclick = async () => {
            valittuKohde = kentta.icao;

            // Hae lentodata kartalle ja näyttöön
            const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${valittuKohde}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=0`);
            lentodata = await res.json();
            console.log(lentodata)

            piirraLento(
              [lentodata.lahto_lat, lentodata.lahto_lon],
              [lentodata.kohde_lat, lentodata.kohde_lon],
              lentodata
            );

            naytaVahvistusNappi(tietokone);
        };
        tietokone.appendChild(nappi);
    });
}

function naytaVahvistusNappi(container) {
    let nappi = document.getElementById("vahvista-lento");
    if (nappi) nappi.remove(); // Poista aiempi jos olemassa

    nappi = document.createElement("button");
    nappi.id = "vahvista-lento";
    nappi.className = "confirm-button";
    nappi.textContent = "[ HYVÄKSY LENTO ]";

    nappi.onclick = async () => {
        try {
            const res = await fetch(`${PALVELIN_OSOITE}/Lentokentta/uusi/?pelaajanID=${pelaajanID}&uusiLentokentta=${valittuKohde}&nykySijainti=${pelaajanTiedot.location}&paivitaPelaaja=1`);
            const result = await res.json();

            pelaajanTiedot = await haePelaajanTiedot();
            paivitaStatit(pelaajanTiedot);

            // Poista vahvistusnappi
            nappi.remove();

            if (valittuKohde === "VTBD") {
                alert("🎉 VOITIT PELIN! Bangkok saavutettu.");
            } else if (pelaajanTiedot.co2_consumed >= pelaajanTiedot.co2_budget) {
                alert("💀 CO₂-budjetti ylitetty. Hävisit pelin.");
            }
        } catch (err) {
            alert("Virhe lennossa: " + err.message);
        }
    };

    container.appendChild(nappi);
}


window.onload = kaynnistaPeli;
