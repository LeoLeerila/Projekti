1. Käyttäjä avaa ```index.html``` tiedoston, josta hänet ohjataan kirjautumaan ```authenticaiton.html``` tiedostoon
2. Käyttäjä valitsee tai tekee uuden pelaajan/profiilin, jonka jälkeen hänet ohjataan ```game.html``` tiedostoon. Osoitteeseen myös lisätään parametri ```user```, jonka arvo on käyttäjän valitseman tai tekemän pelaajan id.
    ```javascript
    //auth.js
    // Käynnistää pelin valitulla profiililla
    function startGameFromSelection() {
    const valittuID = document.getElementById("existing-user").value;
    if (!valittuID) {
        alert("Valitse pelaaja ensin.");
        return;
    }
    // Pelaaja ohjataan game.html urliin ja laitetaan viela parametri user urliin.
    window.location.href = `game.html?user=${valittuID}`;
    }
    ```
3. Aikaisemmassa vaiheessa asetettu ```user``` parametriä hyödynnetään ```game.html``` tiedostossa, jotta voidaan tunnistaa kuka pelaa.
    ```javascript
    //game.js
    pelaajanID = new URLSearchParams(window.location.search).get("user");
    if (!pelaajanID) {
        // Jos url parametria "user" ei ole ohjataan käyttäjä kirjautumaan.
        window.location.href = "authentication.html";
        return;
    }
    ...
    ```
4. Peli logiikka looppi alkaa pyörimään
    ```javascript
    //game.js rivi 46 eteenoäin
    // Aloitetaan peli logiikka
    pelaajanTiedot = await haePelaajanTiedot();
    await paivitaTilastot();
    luoKartta();
    // Aloitetaan lentotietokone eli lentokentän valinta prosessi.
    await haeLentokenttaVaihtoehdot();

    ```

5. Lisää tietoa pelilogiikasta löytyy ```game.js``` -tiedostoon kirjoitetuista kommenteista