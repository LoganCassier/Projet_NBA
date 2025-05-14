import pandas as pd
import os
from datetime import datetime

# Dossier contenant les fichiers Excel
folder_path = r"D:\Projet_perso\ProjetPerso\Data\Trainning_data\2023_2024\Stat_players\Fusion_data"  # Remplace par le chemin de ton répertoire

# Fonction de conversion de date
def convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None  # Gérer les erreurs de format

# Parcourir tous les fichiers Excel du répertoire
for file in os.listdir(folder_path):
    if file.endswith(".xlsx") or file.endswith(".xls"):  # Vérifier si c'est un fichier Excel
        file_path = os.path.join(folder_path, file)

        # Charger le fichier Excel
        df = pd.read_excel(file_path)

        # Vérifier si la colonne GAME_DATE existe
        if "GAME_DATE" in df.columns:
            # Convertir les dates et supprimer les valeurs invalides
            df["GAME_DATE"] = df["GAME_DATE"].astype(str).apply(convert_date)
            df = df.dropna(subset=["GAME_DATE"])  # Supprimer les lignes avec des dates invalides

            # Trier par date croissante
            df = df.sort_values(by="GAME_DATE", ascending=True)

            # Sauvegarder le fichier mis à jour
            df.to_excel(file_path, index=False)
            print(f"✅ Fichier traité : {file}")

print("🚀 Tous les fichiers ont été mis à jour avec succès !")
