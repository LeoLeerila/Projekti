'use strict';
//const response1 = await fetch('http://127.0.0.1:3000/Lentokentta/valitse/?pelaajanID=1')//
//const jsonData1 = await response1.json();//
const Terminal = document.querySelector('#terminal')
const Home = document.querySelector('#homescreen')

let lentoinfo = false;
let pelaajainfo = false;
let athome = true;

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

async function ValitseLkenttä() {
  if (lentoinfo) {
    Terminal.innerHTML = ``;
    Home.innerHTML = ``;
    try {
      const response = await fetch(
          'http://127.0.0.1:3000/Lentokentta/vaihtoehdot/?pelaajanID=1');
      const jsonData = await response.json();
      console.log(jsonData)
      let Data = document.createElement('div');
      for (let i = 0; i < jsonData.lentokenttaLista.length; i++) {
        let P = document.createElement('p')
        P.innerHTML = jsonData.lentokenttaLista[i]
        Data.appendChild(P)}
      Terminal.appendChild(Data)

    } catch (error) {
      console.log(error.message);
  }
  }

}

function HomeScreen () {
  if (athome) {
    Terminal.innerHTML = ``;
    Home.innerHTML = `Terminal`
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
