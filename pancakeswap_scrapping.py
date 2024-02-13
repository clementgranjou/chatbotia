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