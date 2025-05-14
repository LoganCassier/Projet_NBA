import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

'''CE CODE PERMET D EXTRAIRE LES STATS DES JOUEUR POUR LES 5 DERNIER MATCHS DIRECTEMENT DEPUIS LE SITE DE LA NBA AFIN DE POUVOIR DIRECTEMENT PREDIRE LES STATS DU 6EME MACT DE CHAQUE JOUEUR '''

# URL de base des profils joueurs
BASE_URL = "https://www.nba.com/player/{player_id}/{player_name}/profile"

# Recuperation des identifients des joureurs nba a partir des données extraite grace au code extract_names.py

file_path = "Data/last5match/Names_ID_Players.xlsx"
df = pd.read_excel(file_path)

# Créer une liste de dictionnaires avec les colonnes 'ID' et 'Name'
players = df[['ID', 'Name']].dropna().astype(str).apply(lambda row: {"id": row["ID"], "name": row["Name"].lower().replace(" ", "-")}, axis=1).tolist()

# Afficher le résultat
print(players)

def extract_nba_stats(player_id, player_name, output_folder="Data"):
    """
    Extrait les statistiques d'un joueur NBA et les enregistre en fichier Excel.
    :param player_id: str - ID du joueur NBA
    :param player_name: str - Nom formaté du joueur pour l'URL
    :param output_folder: str - Dossier de stockage des fichiers Excel
    """
    try:
        # Construire l'URL du joueur
        url = BASE_URL.format(player_id=player_id, player_name=player_name)

        # Envoyer une requête
        response = requests.get(url)
        response.raise_for_status()

        # Parser la page avec BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraire les tables de statistiques
        tables = pd.read_html(url)

        # Vérifier si des tables ont été trouvées
        if len(tables) == 0:
            print(f"Aucune statistique trouvée pour {player_name}.")
            return

        # Créer le dossier de sortie s'il n'existe pas
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Sauvegarder chaque table en Excel
        for i, table in enumerate(tables):
            file_path = os.path.join(output_folder, f"{player_name}_stats_{i+1}.xlsx")
            table.to_excel(file_path, index=False)
            print(f"Tableau {i+1} pour {player_name} enregistré sous : {file_path}")

    except Exception as e:
        print(f"Erreur pour {player_name} ({player_id}) : {e}")

# Extraire les stats de chaque joueur dans la liste
for player in players:
    extract_nba_stats(player["id"], player["name"])