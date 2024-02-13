from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Scroll vers le bas pour charger toutes les données
while True:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # Attendez un moment pour charger plus de données
    
    # Vérifiez si vous avez atteint la fin de la page
    if "Fin des résultats" in driver.page_source:
        break

# Trouver le tableau
table = driver.find_element(By.TAG_NAME, "table")

# Extraire les données du tableau
table_data = extract_table_data(table)

# Convertir les données en un DataFrame Pandas
df = pd.DataFrame(table_data)

# Afficher les DataFrames
print(df)

# Fermer le navigateur
driver.quit()
