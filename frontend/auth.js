const PALVELIN_OSOITE = "http://127.0.0.1:3000";

// Hakee kaikki pelaajat
async function haeKaikkiPelaajat() {
  const vastaus = await fetch(`${PALVELIN_OSOITE}/Pelaajat/kaikki/`);
  if (!vastaus.ok) {
    throw new Error("Pelaajien haku epäonnistui.");
  }
  const json = await vastaus.json()
  return json;
}

// Luo uusi pelaaja annetulla nimellä
async function luoUusiPelaaja(nimi) {
  const vastaus = await fetch(`${PALVELIN_OSOITE}/Pelaajat/uusi/?nimi=${encodeURIComponent(nimi)}`);
  const data = await vastaus.json();

  if (!vastaus.ok || data.status !== "OK") {
    throw new Error(data.message || "Uuden pelaajan luonti epäonnistui.");
  }

  return data;
}

// Lataa pelaajat valikkoon
async function lataaPelaajatValikkoon() {
  try {
    const pelaajat = await haeKaikkiPelaajat();
    const valikko = document.getElementById("existing-user");

    pelaajat.forEach(p => {
      const vaihtoehto = document.createElement("option");
      vaihtoehto.value = p.id;
      vaihtoehto.textContent = p.screen_name;
      valikko.appendChild(vaihtoehto);
    });
  } catch (virhe) {
    alert("Virhe pelaajien lataamisessa: " + virhe.message);
  }
}

// Käynnistää pelin valitulla profiililla
function startGameFromSelection() {
  const valittuID = document.getElementById("existing-user").value;
  if (!valittuID) {
    alert("Valitse pelaaja ensin.");
    return;
  }
  window.location.href = `game.html?user=${valittuID}`;
}

// Luo uusi käyttäjä ja käynnistää pelin
async function startGameFromNew() {
  const nimi = document.getElementById("new-user").value.trim();
  if (!nimi) {
    alert("Syötä nimi uudelle pelaajalle.");
    return;
  }

  try {
    const uusi = await luoUusiPelaaja(nimi);
    window.location.href = `game.html?user=${uusi.id}`;
  } catch (e) {
    alert("Virhe pelaajaa luodessa: " + e.message);
  }
}

// Tapahtumakuuntelijat painikkeille
window.onload = () => {
  lataaPelaajatValikkoon();
  document.getElementById("btn-load").onclick = startGameFromSelection;
  document.getElementById("btn-create").onclick = startGameFromNew;
};
