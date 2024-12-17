from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Récupération des données météo pour toutes les villes
def get_meteo_data():
    conn = sqlite3.connect("meteo.db")
    cursor = conn.cursor()
    query = """
        SELECT meteo.name, codes.description, meteo.weather, meteo.tmin, meteo.tmax,
               meteo.probarain, meteo.wind10m
        FROM meteo
        JOIN codes ON meteo.weather = codes.code
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Récupération des informations géographiques d'une ville
def get_ville_details(ville):
    conn = sqlite3.connect("meteo.db")
    cursor = conn.cursor()
    query = "SELECT name, insee, latitude, longitude FROM villes WHERE name = ?"
    cursor.execute(query, (ville,))
    data = cursor.fetchone()
    conn.close()
    return data

# Récupération des détails d'un code météo
def get_code_details(code):
    conn = sqlite3.connect("meteo.db")
    cursor = conn.cursor()
    query = "SELECT code, description FROM codes WHERE code = ?"
    cursor.execute(query, (code,))
    data = cursor.fetchone()
    conn.close()
    return data

@app.route("/", methods=["GET"])
def index():
    meteo_data = get_meteo_data()  # Récupérer les données météo
    return render_template("index.html", meteo_data=meteo_data)

@app.route("/ville/<ville>", methods=["GET"])
def ville_details(ville):
    details = get_ville_details(ville)  # Récupérer les détails de la ville
    return render_template("ville_details.html", details=details)

@app.route("/code_meteo/<int:code>", methods=["GET"])
def code_meteo_details(code):
    code_details = get_code_details(code)  # Récupérer les détails du code météo
    return render_template("code_meteo_details.html", code_details=code_details)

if __name__ == "__main__":
    app.run(debug=True)


