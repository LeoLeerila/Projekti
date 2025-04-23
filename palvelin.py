from flask import Flask

from tietokanta import haePelaajanTiedot, nollaaPelaajanTiedot
from lopetus import voitto, havio
from kayttoliittyma import valitseSeuraavaLentokentta
from PeliTehtavat import kysymys

app = Flask(__name__)
@app.route("/tietokanta/haePelaajanTiedot/<int:PelaajanID>")
def tietokanta(PelaajanID):
    

    return vastaus

if __name__ == "__main__":
    app.run(use_reloader=True, host="127.0.0.1", port=3000)