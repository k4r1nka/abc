
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os 
import sqlite3

from flask import g, session
from i18n import TRANSLATIONS, SUPPORTED


app = Flask(__name__, instance_relative_config=True)
app.secret_key = "tajnykluc"

db_path = os.path.join(app.instance_path, "kurzy.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}".replace("\\", "/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.before_request
def set_lang():
    lang = request.args.get("lang")
    if lang not in SUPPORTED:
        lang = session.get("lang", "sk")
    session["lang"] = lang
    g.t = TRANSLATIONS[lang]
    
@app.context_processor
def inject_translations():
    return dict(t=g.t)

class Kurz(db.Model):
    __tablename__ = "Kurzy"
    ID_Kurzu         = db.Column(db.Integer, primary_key = True )
    Nazov_kurzu      = db.Column(db.String)
    Typ_sportu       = db.Column(db.String)
    Max_pocet_ucastnikov  = db.Column(db.Integer )
    ID_trenera       = db.Column(db.Integer )

    def __repr__(self):
        return f"<kurz {self.Nazov_kurzu}>"
    
class Trener(db.Model):
    __tablename__ = "Treneri"
    ID_trenera    = db.Column(db.Integer, primary_key = True )
    Meno          = db.Column(db.String)
    Priezvisko    =  db.Column(db.String)
    Specializacia =  db.Column(db.String)
    Telefon       = db.Column(db.String)

    def __repr__(self):
        return f"<trener {self.ID_trenera}>"
    
class Miesto(db.Model):
    __tablename__ = "Miesta"
    ID_miesta     = db.Column(db.Integer, primary_key = True )
    Nazov_miesta  = db.Column(db.String)
    Adresa        = db.Column(db.String)
    Kapacita      = db.Column(db.Integer)

    def __repr__(self):
        return f"<miesto {self.ID_miesta}>"

class Maxkap(db.Model):
    __tablename__         = "Maxkap"
    Max_pocet_ucastnikov  = db.Column(db.Integer)
    ID_kurzu              = db.Column(db.Integer, primary_key = True)

    def __repr__(self):
        return f"<maxkap {self.ID_kurzu}>"


def data():
    conn = sqlite3.connect("kurzy.db")
    return conn

@app.route('/')  
def index():
    return render_template("home.html")
        

@app.route('/kurzy')  
def zobraz_kurzy():
    kurzy = Kurz.query.all()
    return render_template("kurzy.html", kurzy=kurzy)


@app.route('/treneri')  
def zobraz_trenerov():
    treneri = Trener.query.all()
    return render_template("treneri.html",treneri = treneri)


@app.route('/miesta')
def miesta():
    miesta = Miesto.query.all()
    return render_template("miesta.html",miesta = miesta)


@app.route('/max_kap')
def kapacita():
    kapacita = Maxkap.query.all()
    return render_template("maxkap.html",max_kap = kapacita)


if __name__ == '__main__':
    app.run(debug=True)


