import csv
import html
import sys
from pathlib import Path

def csv_to_html(csv_file_path, html_file_path):
    try:
        csv_path = Path(csv_file_path)
        if not csv_path.exists():
            print(f"Erreur : le fichier '{csv_file_path}' est introuvable.")
            return

        # Lecture du CSV
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            print("Erreur : le fichier CSV est vide.")
            return

        # Construction du HTML
        html_content = [
            "<!DOCTYPE html>",
            "<html lang='fr'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <title>Tableau d'emplois</title>",
            "    <style>",
            "        table { border-collapse: collapse; width: 100%; }",
            "        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }",
            "        th { background-color: #f2f2f2; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <h1>Contenu du fichier CSV</h1>",
            "    <table>"
        ]

        # Ligne d'en-tête
        html_content.append("        <tr>")
        for header in rows[0]:
            html_content.append(f"            <th>{html.escape(header)}</th>")
        html_content.append("        </tr>")

        # Lignes de données
        for row in rows[1:]:
            html_content.append("        <tr>")
            for cell in row:
                html_content.append(f"            <td>{html.escape(cell)}</td>")
            html_content.append("        </tr>")

        html_content.extend([
            "    </table>",
            "</body>",
            "</html>"
        ])

        # Écriture du fichier HTML
        with open(html_file_path, "w", encoding="utf-8") as htmlfile:
            htmlfile.write("\n".join(html_content))

        print(f"Conversion réussie : '{html_file_path}' créé.")

    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(" les parametres de la fonction sont manquantes")
        print("Utilisation : python csv_to_html.py fichier.csv fichier.html")
    else:
        csv_to_html(sys.argv[1], sys.argv[2])
