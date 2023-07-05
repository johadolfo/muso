import sqlite3
import xlsxw
riter

# Connexion à la base de données SQLite
conn = sqlite3.connect('nom_de_la_base_de_données.db')

# Création d'un objet Workbook
workbook = xlsxwriter.Workbook('nom_du_fichier.xlsx')

# Récupération de la liste des tables dans la base de données
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Parcours de chaque table et stockage dans une feuille Excel distincte
for table_name in tables:
    worksheet = workbook.add_worksheet(table_name[0])
    cursor.execute(f"SELECT * FROM {table_name[0]}")
    rows = cursor.fetchall()
    for row_num, row in enumerate(rows):
        for col_num, cell_value in enumerate(row):
            worksheet.write(row_num, col_num, cell_value)

# Fermeture du fichier Excel et de la connexion à la base de données
workbook.close()
conn.close()