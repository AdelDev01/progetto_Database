import os
import pandas as pd
from py2neo import Graph, Node, Relationship

csv_directory = 'C:/Users/shata/OneDrive/Desktop/Development/LINGUAGGIO_PYTHON/Progetto_Database'

db100 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db100")
db75 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db75")
db50 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db50")
db25 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db25")


db_percentuali = {
    100: db100,
    75: db75,
    50: db50,
    25: db25
}

csv_files = ['utenti_25.csv', 'utenti_50.csv', 'utenti_75.csv', 'utenti_100.csv',
            'commercianti_25.csv', 'commercianti_50.csv', 'commercianti_75.csv', 'commercianti_100.csv',
            'transazioni_25.csv', 'transazioni_50.csv', 'transazioni_75.csv', 'transazioni_100.csv']

# Importa i dati dai file CSV nei grafi Neo4j e crea i nodi
for csv_file in csv_files:
    for percentuale, graph in db_percentuali.items():
            if str(percentuale) in csv_file:

                # Percorso completo al file CSV
                csv_path = os.path.join(csv_directory, csv_file)

                # Leggi i dati dal file CSV utilizzando pandas
                data = pd.read_csv(csv_path)

                if 'utenti' in csv_file:
                    for index, row in data.iterrows():
                        user_node = Node("Utente", **row.to_dict())
                        graph.create(user_node)

                elif 'commercianti' in csv_file:
                    for index, row in data.iterrows():
                        merchant_node = Node("Commerciante", **row.to_dict())
                        graph.create(merchant_node)

                elif 'transazioni' in csv_file:
                    for index, row in data.iterrows():
                        transaction_node = Node("Transazione", **row.to_dict())
                        graph.create(transaction_node)

                        
                            # Crea la relazione tra Utente e Transazione
                        user_id = row['id_utente']
                        user_node = graph.nodes.match("Utente", id_utente=user_id).first()
                        if user_node:
                            relationship = Relationship(user_node, 'HA_EFFETTUATO', transaction_node)
                            graph.create(relationship)
                                
                        merchant_id = row['id_commerciante']
                        merchant_node = graph.nodes.match('Commerciante',id = merchant_id).first()
                        if merchant_node:
                            merchant_relationship = Relationship(transaction_node, 'PRESSO', merchant_node)
                            graph.create(merchant_relationship)

                print(f"Dati del file CSV {csv_file} inseriti in Neo4j per il database {graph} con successo.")
            else:  
                pass