from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


# Initialisation du WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL de la page à scraper
url = 'https://coinmarketcap.com/fr/'

# Accéder à la page
driver.maximize_window()
driver.get(url)

# Attendre que la page soit chargée
time.sleep(5)

# Trouver tous les tableaux de la page
tables = driver.find_elements(By.TAG_NAME, "table")

# Fonction pour extraire les données d'un tableau
def extract_table_data(table):
    data = []
    # Trouver les en-têtes de colonnes
    headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]
    
    # Trouver toutes les lignes du tableau
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    # Extraire les données de chaque ligne
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = {}
            for i, cell in enumerate(cells):
                row_data[headers[i]] = cell.text
            data.append(row_data)
    
    return data

# Extraire les données de chaque tableau
table_data = [extract_table_data(table) for table in tables]
# Convertir les données en DataFrames Pandas
dataframes = [pd.DataFrame(data) for data in table_data]


# Fermer le navigateur
driver.quit()


# Afficher les DataFrames
for i, df in enumerate(dataframes):
    print(f"DataFrame {i+1}:")
    print(df.head(50))
    print("\n")




df.to_csv('df_CoinMarketCap.csv')

# # Afficher les données extraites
# for i, data in enumerate(table_data):
#     print(f"Tableau {i+1}:")
#     for row in data:
#         print(row)
#     print("\n")

# dataframes