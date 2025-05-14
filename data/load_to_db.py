
import pandas as pd
import sqlite3

# Charger le fichier CSV nettoyé
df = pd.read_csv("data/European_Player_Stats_2020-2021.csv")

# Connexion à une base SQLite
conn = sqlite3.connect("data/players.db")

# Enregistrement dans une table
df.to_sql("players", conn, if_exists="replace", index=False)

print("✅ Données chargées dans data/players.db")
