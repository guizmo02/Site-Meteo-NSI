from urllib.request import urlopen
import json
import sqlite3

# Configuration de l'API
token = '8678ccc4e75162ee8ccd432bd966b0c35bc2c38be6015c557c7636a6545e71f3'

# Liste des villes avec leurs codes INSEE
villes = {
    "Laon": "02408",
    "Biarritz": "64122"
}

# Connexion à la base de données SQLite
conn = sqlite3.connect("meteo.db")
cursor = conn.cursor()

# Création de la table villes pour les informations géographiques
cursor.execute("""
CREATE TABLE IF NOT EXISTS villes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    insee TEXT,
    latitude REAL,
    longitude REAL
)
""")

# Création de la table meteo pour les prévisions
cursor.execute("""
CREATE TABLE IF NOT EXISTS meteo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weather INTEGER,
    tmin REAL,
    tmax REAL,
    probarain REAL,
    wind10m REAL
)
""")

# Création de la table codes pour les descriptions météorologiques
cursor.execute("""
CREATE TABLE IF NOT EXISTS codes (
    code INTEGER PRIMARY KEY,
    description TEXT
)
""")

# Insertion des codes météorologiques
codes_meteo = [
    (0, "Soleil"), (1, "Peu nuageux"), (2, "Ciel voilé"), (3, "Nuageux"), (4, "Très nuageux"),
    (5, "Couvert"), (6, "Brouillard"), (7, "Brouillard givrant"), (10, "Pluie faible"),
    (11, "Pluie modérée"), (12, "Pluie forte"), (13, "Pluie faible verglaçante"),
    (14, "Pluie modérée verglaçante"), (15, "Pluie forte verglaçante"), (16, "Bruine"),
    (20, "Neige faible"), (21, "Neige modérée"), (22, "Neige forte"),
    (30, "Pluie et neige mêlées faibles"), (31, "Pluie et neige mêlées modérées"),
    (32, "Pluie et neige mêlées fortes"), (40, "Averses de pluie locales et faibles"),
    (41, "Averses de pluie locales"), (42, "Averses locales et fortes"),
    (43, "Averses de pluie faibles"), (44, "Averses de pluie"), (45, "Averses de pluie fortes"),
    (46, "Averses de pluie faibles et fréquentes"), (47, "Averses de pluie fréquentes"),
    (48, "Averses de pluie fortes et fréquentes"), (60, "Averses de neige localisées et faibles"),
    (61, "Averses de neige localisées"), (62, "Averses de neige localisées et fortes"),
    (63, "Averses de neige faibles"), (64, "Averses de neige"), (65, "Averses de neige fortes"),
    (66, "Averses de neige faibles et fréquentes"), (67, "Averses de neige fréquentes"),
    (68, "Averses de neige fortes et fréquentes"), (70, "Averses de pluie et neige mêlées localisées et faibles"),
    (71, "Averses de pluie et neige mêlées localisées"), (72, "Averses de pluie et neige mêlées localisées et fortes"),
    (73, "Averses de pluie et neige mêlées faibles"), (74, "Averses de pluie et neige mêlées"),
    (75, "Averses de pluie et neige mêlées fortes"), (76, "Averses de pluie et neige mêlées faibles et nombreuses"),
    (77, "Averses de pluie et neige mêlées fréquentes"), (78, "Averses de pluie et neige mêlées fortes et fréquentes"),
    (100, "Orages faibles et locaux"), (101, "Orages locaux"), (102, "Orages fort et locaux"),
    (103, "Orages faibles"), (104, "Orages"), (105, "Orages forts"), (106, "Orages faibles et fréquents"),
    (107, "Orages fréquents"), (108, "Orages forts et fréquents"),
    (120, "Orages faibles et locaux de neige ou grésil"), (121, "Orages locaux de neige ou grésil"),
    (122, "Orages locaux de neige ou grésil"), (123, "Orages faibles de neige ou grésil"),
    (124, "Orages de neige ou grésil"), (125, "Orages de neige ou grésil"),
    (126, "Orages faibles et fréquents de neige ou grésil"), (127, "Orages fréquents de neige ou grésil"),
    (128, "Orages fréquents de neige ou grésil"), (130, "Orages faibles et locaux de pluie et neige mêlées ou grésil"),
    (131, "Orages locaux de pluie et neige mêlées ou grésil"),
    (132, "Orages fort et locaux de pluie et neige mêlées ou grésil"),
    (133, "Orages faibles de pluie et neige mêlées ou grésil"),
    (134, "Orages de pluie et neige mêlées ou grésil"),
    (135, "Orages forts de pluie et neige mêlées ou grésil"),
    (136, "Orages faibles et fréquents de pluie et neige mêlées ou grésil"),
    (137, "Orages fréquents de pluie et neige mêlées ou grésil"),
    (138, "Orages forts et fréquents de pluie et neige mêlées ou grésil"), (140, "Pluies orageuses"),
    (141, "Pluie et neige mêlées à caractère orageux"), (142, "Neige à caractère orageux"),
    (210, "Pluie faible intermittente"), (211, "Pluie modérée intermittente"),
    (212, "Pluie forte intermittente"), (220, "Neige faible intermittente"),
    (221, "Neige modérée intermittente"), (222, "Neige forte intermittente"),
    (230, "Pluie et neige mêlées"), (231, "Pluie et neige mêlées"),
    (232, "Pluie et neige mêlées"), (235, "Averses de grêle")
]

cursor.executemany("INSERT OR IGNORE INTO codes (code, description) VALUES (?, ?)", codes_meteo)

# Fonction pour insérer les informations géographiques des villes
def inserer_ville(ville, insee):
    url = f'https://api.meteo-concept.com/api/forecast/daily?token={token}&insee={insee}'
    retour = urlopen(url).read()
    dico = json.loads(retour)

    latitude = dico.get("city", {}).get("latitude")
    longitude = dico.get("city", {}).get("longitude")

    cursor.execute("INSERT OR IGNORE INTO villes (name, insee, latitude, longitude) VALUES (?, ?, ?, ?)",
                   (ville, insee, latitude, longitude))

    # Insertion des prévisions dans la table meteo
    for jour in dico.get("forecast", []):
        cursor.execute("""
        INSERT INTO meteo (name, weather, tmin, tmax, probarain, wind10m)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (ville, jour.get("weather"), jour.get("tmin"), jour.get("tmax"),
              jour.get("probarain"), jour.get("wind10m")))

# Insérer les informations des villes
for ville, insee in villes.items():
    inserer_ville(ville, insee)

# Sauvegarde des modifications et fermeture de la connexion
conn.commit()
conn.close()
print("Rendu final : Les données météo et les descriptions ont été insérées avec succès.")



