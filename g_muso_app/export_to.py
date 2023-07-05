import sqlite3
import csv

# Connexion à la base de données SQLite
conn = sqlite3.connect('g_notes.db')

# Récupération de la liste des tables dans la base de données
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Parcours de chaque table et stockage dans un fichier CSV distinct
for table_name in tables:
    with open(f"{table_name[0]}.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()
        for row_num, row in enumerate(rows):
            csv_writer.writerow(row)

# Fermeture de la connexion à la base de données
conn.close()