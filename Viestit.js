"use strict"

const otsikko = "WHATSAPP(1)"

    const greetings = [
     "NYT PE#%!#* KOTIIN SIELTÄ! 😡",
  "Jos et vastaa kohta, laitan susta ilmoituksen kadonneeksi. Ja ehkä Tinderiin. 😉",
  "Mä en ole katkera, mä olen katkeran mestari. 🍋",
  "Sun puhelin toimii siellä, vai söikö lisko senkin? 🦎📵",
  "Toivottavasti sulla on kivaa siellä – täällä meillä on tiskit, lapset ja hiljainen raivo. 🧼👶😑",
  "Kyllä se on jännä miten nopeasti mies muistaa vastata kun kotiavaimet katoaa... 😏",
  "Kello käy, pinna kiristyy, wifi toimii – joten mikset sinä? ⏰📶🔥",
  "Jos haluat elää kuin sinkku, niin kai mäkin voin alkaa käyttäytyä kuin ex-vaimo. 💅",
  "Eikö ollutkaan pelkkä 'rentoutumisreissu'? No niin minäkin sanoin kun menin Ikeaan yksin. 🛋️🛒",
  "Vastaa ennen kuin käännän tämän lomareissun Netflix-dokumentiksi nimeltä *Mies joka ei palannut*. 🎥",
  "Muista että rakastan sua... mutta rakkaus ei suojaa sua, jos et laita viestiä NYT. ❤️🪓",
  "Onko siellä niin paljon palmuja, ettet näe omaa järkeäsi enää? 🌴🙄",
  "Tässä minä yksin kotona, seurana vain sarkasmi ja kylmä kahvi. ☕️🧊",
  "Aika jännä – sulla on aikaa juoda drinkkejä, muttei lähettää yhtä viestiä. Prioriteetit kohdallaan! 🍹📲",
  "Sanoin että mene lomalle, en että unohda että oot naimisissa. 🔔💍"

    ];


    document.addEventListener("DOMContentLoaded", () => {
      const title = document.getElementById('title');
      title.innerText = otsikko
    });


    function openForm() {
      document.getElementById("myForm").style.display = "block";
      appendToDisplay();
    }

    // Piilota lomake ja tyhjennä viesti
    function closeForm() {
      document.getElementById("myForm").style.display = "none";
      const display = document.querySelector("textarea[name='msg']");
      if (display) display.value = "";
    }


    function appendToDisplay() {
      const display = document.querySelector("textarea[name='msg']");
      const newId = Math.floor(Math.random() * greetings.length);
      display.value = greetings[newId];
    }




