from nba_api.stats.endpoints import LeagueGameLog
import pandas as pd

def get_current_season_nba_games():
    # Récupérer tous les matchs de la saison 2023-24
    game_log = LeagueGameLog(season="2023-24", season_type_all_star='Regular Season')

    # Convertir les résultats en DataFrame
    df = game_log.get_data_frames()[0]

    # Sélectionner uniquement les statistiques importantes
#    df = df[['GAME_ID', 'TEAM_NAME', 'MATCHUP', 'PTS', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV']]

    return df

# Exécuter le script et afficher les 10 premiers matchs
season_games = get_current_season_nba_games()
season_games.to_excel(r"D:\Projet_perso\ProjetPerso\Data\Trainning_data\2023_2024\Stat_teams\team_match_results.xlsx", index=False)
print(season_games.head(10))
