import os
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['db_frodi']

percentuali =  [100,75,50,25]
data_types = ['transazioni','utenti','commercianti']


for percentuale in percentuali:
    for data_type in data_types:
        collection_name = f'{data_type}_{percentuale}'
        csv_filename = f'{data_type}_{percentuale}.csv'

        script_directory = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_directory, csv_filename)

        data = pd.read_csv(csv_path, encoding='ISO-8859-1')
        data_json = data.to_dict(orient='records')

        collection = db[collection_name]
        collection.insert_many(data_json)

        print(f"Dati del dataset {collection_name} inseriti in MongoDB con successo.")

print("Inserimento completato per tutti i dataset.")