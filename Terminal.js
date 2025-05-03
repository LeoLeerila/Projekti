'use strict';
//const response1 = await fetch('http://127.0.0.1:3000/Lentokentta/valitse/?pelaajanID=1')//
//const jsonData1 = await response1.json();//
const Terminal = document.querySelector('#terminal')
const Home = document.querySelector('#homescreen')

let game = true;
let lentoinfo = false;
let pelaajainfo = false;
let athome = true;
let lento = false;
let kyssari = false;
let nykysijainti = 'x';
let lentosijainti = 'y';
let nykymaa = 'z';


async function HaePelaajantiedot() {
  if (pelaajainfo) {
    Terminal.innerHTML = ``;
    Home.innerHTML = ``;
    try {
      const response = await fetch('http://127.0.0.1:3000/PelaajanTiedot/hae/?pelaajanID=1');
      const jsonData = await response.json();
      console.log(jsonData)
      for (const [key, value] of Object.entries(jsonData)) {
        let Data = document.createElement('p')
        Data.innerHTML = [key, value];
        Terminal.appendChild(Data)

      }
      const Back = document.createElement('h2')
      Back.innerHTML = `Back`
      Back.addEventListener("click", function() {
          pelaajainfo = false;
          athome = true;
          console.log('return')
          HomeScreen()
      });
    Terminal.appendChild(Back)
    } catch (error) {
        console.log(error.message);
    }

  }
  else {
    pelaajainfo = false;
    athome = true;
  }
}

async function Lenna() {
  if (game) {
    Terminal.innerHTML = ``;
    Home.innerHTML = ``;
    try {
      const response = await fetch(`http://127.0.0.1:3000/Lentokentta/uusi/?pelaajanID=1&uusiLentokentta=${lentosijainti}&nykySijainti=${nykysijainti}&paivitaPelaaja=1`);
      const jsonData = await response.json();
      console.log(jsonData)
      Kysymys()
    } catch (error) {
      console.log(error.message);
  }
  }
}

function Kysymys() {
  Terminal.innerHTML = ``;
  Home.innerHTML = ``;
  Hae()
  let p = document.createElement('h2')
  p.innerHTML = `Jos haluat jatkaa, joudut vastaamaan kysymykseen:`;
  Terminal.appendChild(p);
}

async function ValitseLkenttä() {
  if (game) {
    Terminal.innerHTML = ``;
    Home.innerHTML = ``;
    try {
      const response = await fetch(
          'http://127.0.0.1:3000/Lentokentta/vaihtoehdot/?pelaajanID=1');
      const jsonData = await response.json();
      console.log(jsonData)
      let Data = document.createElement('div');
      nykymaa = jsonData.nykySijainti
      let nyky = document.createElement('h2')
      nyky.innerHTML = `Tämänhetkinen maa: ` + nykymaa;
      Terminal.appendChild(nyky)
      for (let i = 0; i < jsonData.lentokenttaLista.length; i++) {
        let P = document.createElement('p')
        lentosijainti = jsonData.lentokenttaLista[i][1];
        P.innerHTML = jsonData.lentokenttaLista[i];
        P.addEventListener("click", function() {
          lento = true;
          lentoinfo = false;
          Lenna();
        });
        Data.appendChild(P)}
      Terminal.appendChild(Data)

    } catch (error) {
      console.log(error.message);
  }
  }

}
async function Hae() {
  try {
    const response = await fetch('http://127.0.0.1:3000/PelaajanTiedot/hae/?pelaajanID=1');
    const jsonData = await response.json();
    console.log(jsonData)
    nykysijainti = jsonData.location;
    console.log('location check')

  } catch (error) {
      console.log(error.message);
  }

}

async function HomeScreen () {
  try {
    const response = await fetch('http://127.0.0.1:3000/PelaajanTiedot/nollaa/?pelaajanID=1');
    const jsonData = await response.json();
  } catch (error) {
      console.log(error.message);
  }
  if (athome) {
    Terminal.innerHTML = ``;
    Home.innerHTML = `Terminal`
    Hae()
    const Fly = document.createElement('h2')
    Fly.innerHTML = `Pelaaja`
    const Playeri = document.createElement('h2')
    Playeri.innerHTML = `Lennä`
    Fly.addEventListener("click", function() {
      pelaajainfo = true;
      athome = false;
      HaePelaajantiedot()
    });
    Terminal.appendChild(Fly)
    Playeri.addEventListener("click", function() {
      lentoinfo = true;
      athome = false;
      ValitseLkenttä()
    });
    Terminal.appendChild(Playeri)
  }
}
HomeScreen()
