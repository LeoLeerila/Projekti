'use strict';

const Terminal = document.querySelector('#terminal')
const Home = document.querySelector('#homescreen')

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
  Terminal.innerHTML = ``;
  Home.innerHTML = ``;
  try {
    const response = await fetch('');
    const jsonData = await response.json();
    console.log(jsonData)
  } catch (error) {
    console.log(error.message);
  }

}

function HomeScreen () {
  if (athome) {
    Terminal.innerHTML = ``;
    Home.innerHTML = `Terminal`
    const Fly = document.createElement('h2')
    Fly.innerHTML = `Pelaaja`
    Fly.addEventListener("click", function() {
      pelaajainfo = true;
      athome = false;
      HaePelaajantiedot()
    });
    Terminal.appendChild(Fly)
  }
}
HomeScreen()
