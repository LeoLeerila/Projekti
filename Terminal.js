'use strict';

async function HaeLentokenttä() {
  Terminal.innerHTML = ``;
  try {
    const response = await fetch('http://127.0.0.1:3000/PelaajanTiedot/hae/?pelaajanID=1');    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();
    console.log(jsonData)
    for (const [key, value] of Object.entries(jsonData)) {
      let Data = document.createElement('p')
      Data.innerHTML = [key, value];
      Terminal.appendChild(Data)

    }


  } catch (error) {
        console.log(error.message);
    }

}
const Terminal = document.querySelector('#terminal')
const Fly = document.createElement('button')
Fly.innerHTML = `Pelaaja`
Fly.addEventListener("click", function() {
  HaeLentokenttä();
});
Terminal.appendChild(Fly)