from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players
import pandas as pd
import os
import time

# Définition du dossier d'enregistrement
output_dir = r"D:\Projet_perso\ProjetPerso\Data\Trainning_data\2024_2025\Stat_players"
os.makedirs(output_dir, exist_ok=True)

# Nom du fichier final fusionné
fichier_fusionne = os.path.join(output_dir, "stats_joueurs_fusionnees.xlsx")


def get_all_games_stats(player_id, player_name, season="2023-24"):
    """Récupère les statistiques des matchs pour un joueur NBA donné."""
    try:
        game_log = PlayerGameLog(player_id=player_id, season=season)
        df = game_log.get_data_frames()[0]
        df = df.sort_values(by="GAME_DATE", ascending=False)

        return df
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des stats de {player_name}: {e}")
        return None


def save_all_players_stats(season="2024-25"):
    """Télécharge et enregistre les stats de tous les joueurs NBA pour la saison donnée."""
    nba_players = players.get_active_players()  # Liste des joueurs actifs

    print(f"📊 Récupération des stats pour {len(nba_players)} joueurs...")

    for player in nba_players:
        player_id = player['id']
        player_name = player['full_name']

        print(f"🔍 Traitement de {player_name}...")

        stats_df = get_all_games_stats(player_id, player_name, season)

        if stats_df is not None and not stats_df.empty:
            # Nettoyer le nom du fichier
            safe_player_name = player_name.replace(" ", "_").replace(".", "").replace("'", "")
            file_path = os.path.join(output_dir, f"{safe_player_name}.xlsx")

            # Enregistrer au format Excel
            stats_df.to_excel(file_path, index=False)
            print(f"✅ Statistiques enregistrées pour {player_name} -> {file_path}")

        # Pause pour éviter les limites de requêtes de l'API
        time.sleep(1)

    print("🎉 Toutes les statistiques ont été récupérées et enregistrées avec succès !")


def merge_all_excel_files():
    """Fusionne tous les fichiers Excel du dossier en un seul, avec une colonne pour le nom du joueur et le fichier source."""
    df_list = []

    for fichier in os.listdir(output_dir):
        if fichier.endswith(".xlsx") and fichier != "stats_joueurs_fusionnees.xlsx":
            chemin_fichier = os.path.join(output_dir, fichier)

            # Lecture du fichier
            df = pd.read_excel(chemin_fichier)

            # Extraction du nom du joueur à partir du nom de fichier
            nom_joueur = fichier.replace(".xlsx", "").replace("_", " ")

            # Ajout des nouvelles colonnes
            df["Nom_Joueur"] = nom_joueur
            df["Nom_Fichier"] = fichier

            # Ajout à la liste
            df_list.append(df)

    if df_list:
        # Fusionner tous les fichiers en un seul DataFrame
        df_fusionne = pd.concat(df_list, ignore_index=True)

        # Sauvegarde dans un unique fichier Excel
        df_fusionne.to_excel(fichier_fusionne, index=False)
        print(f"📂 Fusion terminée ! Fichier enregistré sous : {fichier_fusionne}")
    else:
        print("⚠️ Aucun fichier Excel trouvé pour la fusion.")


# Exécution du script
save_all_players_stats()  # Étape 1 : Télécharger les stats des joueurs
merge_all_excel_files()   # Étape 2 : Fusionner tous les fichiers en un seul
