# Algo de scrapping CoinMarketCap




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







# Algo de scrapping PancakeSwap




from selenium import webdriver
from selenium.webdriver.edge.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
 
 
ua = UserAgent()
user = ua.getChrome["useragent"]
print(user)
chrome_options = Options()  
chrome_options.add_argument("--enable-javascript")
 
 
#chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--user-agent={user}")
 
driver = webdriver.Edge(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(350)
driver.get("https://pancakeswap.finance/farms")
 
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
 
 
print("test")
element = wait.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="table-container"]/div/table'))))
element.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr')
print(element)
#rows = element.find_element(By.XPATH, '//*[@id="table-container"]/div/table/tbody/tr').get_attribute('outerHTML')
 
 
lignes = element.find_elements(By.TAG_NAME, 'tr')
 
# Initialiser une liste pour stocker les données
donnees_tableau = []
 
# Boucler sur chaque ligne
for ligne in lignes:
    # Récupérer les cellules de la ligne
    cellules = ligne.find_elements(By.TAG_NAME, 'td')
    autre = ligne.find_elements(By.TAG_NAME, 'tr')
    apr = cellules.find_elements(By.TAG_NAME, '//*[@id="table-container"]/div/table/tbody/tr[1]/td[3]/div/div/div[2]/div/div/div/div/div[1]')
   
    
    # Initialiser une liste pour stocker les données de la ligne
    donnees_ligne = []
    
    # Boucler sur chaque cellule
    for cellule in cellules:
        # Ajouter le texte de la cellule à la liste de la ligne
        donnees_ligne.append(cellule.text)
    
    # Ajouter les données de la ligne au tableau global
    donnees_tableau.append(donnees_ligne)
 
# Afficher les données du tableau
for ligne in donnees_tableau:
    print(ligne)
 
#driver.quit()