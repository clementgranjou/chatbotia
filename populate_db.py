import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import csv

# Configuration - Replace with your details
api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {'X-CMC_PRO_API_KEY': '342c289d-a106-458d-85e6-71f5fb5fe0c9'}
db_config = {
    'host': 'localhost',
    'database': 'cryptocurrency',
    'user': 'root',
    'password': 'Clemdigi3'
}

def export_data_to_csv(connection, filename):
    cursor = connection.cursor()
    query = "SELECT * FROM cryptocurrency"
    cursor.execute(query)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Écrire les en-têtes de colonnes
        csvwriter.writerow([i[0] for i in cursor.description])
        # Écrire les données
        csvwriter.writerows(cursor)

    cursor.close()
    print(f"Les données ont été exportées dans le fichier {filename}")


def convert_iso_to_mysql(date_string):
    # Convertit une date ISO 8601 en format compatible MySQL.
    if date_string:
        return datetime.fromisoformat(date_string.rstrip('Z')).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

def fetch_data_from_api(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data from API")
        return None

def connect_to_database(host, database, user, password):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def insert_data_to_db(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO cryptocurrency (Id, Name, Symbol, Slug, num_market_pairs, date_added, 
                                max_supply, circulating_supply, total_supply, price, 
                                volume_24h, volume_change_24h, percent_change_1h, 
                                percent_change_24h, percent_change_7d, percent_change_30d, 
                                percent_change_60d, percent_change_90d, market_cap, 
                                market_cap_dominance, fully_diluted_market_cap)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for coin in data['data']:
        date_added = convert_iso_to_mysql(coin['date_added'])
        values = (coin['id'], coin['name'], coin['symbol'], coin['slug'], coin['num_market_pairs'], 
                  date_added, coin['max_supply'], coin['circulating_supply'], coin['total_supply'],
                  coin['quote']['USD']['price'], coin['quote']['USD']['volume_24h'], coin['quote']['USD']['volume_change_24h'], 
                  coin['quote']['USD']['percent_change_1h'], coin['quote']['USD']['percent_change_24h'], 
                  coin['quote']['USD']['percent_change_7d'], coin['quote']['USD']['percent_change_30d'], 
                  coin['quote']['USD']['percent_change_60d'], coin['quote']['USD']['percent_change_90d'], 
                  coin['quote']['USD']['market_cap'], coin['quote']['USD']['market_cap_dominance'], 
                  coin['quote']['USD']['fully_diluted_market_cap'])
        cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()


# Main Execution
data = fetch_data_from_api(api_url, headers)
if data:
    connection = connect_to_database(**db_config)
    if connection:
        insert_data_to_db(connection, data)
        export_data_to_csv(connection, 'cryptocurrency_data.csv')
        connection.close()
