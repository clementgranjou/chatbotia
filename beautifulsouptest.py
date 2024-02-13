import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page à scraper
url = 'https://coinmarketcap.com/fr/'

# Télécharger la page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver le tableau dans la page - ajustez le sélecteur si nécessaire
table = soup.find('table') 

# Extraire les en-têtes de colonnes
headers = []
for header in table.find_all('th'):
    headers.append(header.text.strip())

# Extraire les données de chaque ligne
rows = table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if cols:  # Assurez-vous que la ligne contient des colonnes
        data.append(cols)

# Créer un DataFrame avec les données
df = pd.DataFrame(data, columns=headers)

# Afficher le DataFrame
print(df.head(50))
