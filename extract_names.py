import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import os


# URL de la page web à analyser
url = 'https://www.nba.com/players'
list_name = []
list_id = []

# Envoyer une requête GET à l'URL
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trouver le script avec l'ID __NEXT_DATA__
    script_tag = soup.find('script', id='__NEXT_DATA__')

    # Vérifier si le script a été trouvé
    if script_tag:
        # Extraire le contenu JSON
        json_data = json.loads(script_tag.string)

        # Maintenant, vous pouvez accéder aux éléments du JSON
        # Par exemple, si vous voulez extraire un élément spécifique comme 'props'
        if 'props' in json_data:
            props = json_data['props']

        # Si vous voulez extraire un élément plus profond, vous pouvez continuer à naviguer dans le JSON
        # Par exemple, pour accéder à 'pageProps' dans 'props'
        if 'pageProps' in props:
            page_props = props['pageProps']
            data_players = page_props["players"]

            for ind_player in range(len(data_players)):

                list_name.append(data_players[ind_player]["PLAYER_SLUG"])
                list_id.append(data_players[ind_player]["PERSON_ID"])
    else:
        print("Script __NEXT_DATA__ non trouvé")

# Créer un DataFrame à partir des listes

df = pd.DataFrame({
    'Name': list_name,
    'ID': list_id
})

# Chemin complet du fichier Excel
# Sauvegarder le DataFrame en fichier Excel

chemin_fichier_excel = os.path.join('Data', 'Names_ID_Players.xlsx')
df.to_excel(chemin_fichier_excel, index=False)

print(list_name)