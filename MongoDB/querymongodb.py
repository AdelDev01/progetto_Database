import csv
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
from scipy import stats



def calculate_confidence_interval(data):
    confidence = 0.95
    n = len(data)
    mean_value = np.mean(data)
    stderr = stats.sem(data)
    margin_of_error = stderr * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean_value, margin_of_error

percentuali = [25,50,75,100]

# Connessione al database MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['db_frodi']

first_response_time = {}
average_response_time = {}
response_time = []

# Query 1: Tutte le transazioni in ordine crescente superiore ai 1500 euro e minore di 2500 euro

def find_transactions_ordered_by_amount(transactions_collection):
    start_time = time.time()
    pipeline = [
        
        {
            '$match': {
                'importo': {'$gte': 1500, '$lte': 2500}  # Filtra per importi maggiori o uguali a 1500 e minore di 2500 euro
            }
        },
        {
            '$sort': {'importo': 1}  # Ordina per importo crescente
        },
        {
            '$project': {
                '_id': 0,
                'importo': 1
            }
        }
    ]

    results = list(db[transactions_collection].aggregate(pipeline))
    if results:
        for result in results:
            print(result)  # Stampa le transazioni ordinate per importo crescente superiore ai 1500 euro
    else:
        print("Nessuna transazione trovata")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 1): {first_execution_time} ms")

    # Aggiungi il tempo di risposta medio della prima esecuzione al dizionario per la prima query
    first_response_time[f"{percentuale} - Query 1"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        results = list(db[transactions_collection].aggregate(pipeline))
        end_time = time.time()
        tempo_esecuzione = round((end_time - start_time) * 1000, 2)
        response_time.append(tempo_esecuzione)
    
    next_average_time = round((sum(response_time) / len(response_time)), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 1): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 1): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")

    average_response_time[f"{percentuale} - Query 1"] = (next_average_time, mean, margin_of_error)

# Query 2: Trova il numero di transazioni di un utente di nome Kevin Sanders

def find_transactions_per_user(users_collection):
    start_time = time.time()

    pipeline = [
    {
        '$match': {
            'nome': 'Kevin',
            'cognome': 'Sanders'
        }
    },
    {
        '$lookup': {
            'from': f'transazioni_{percentuale}',  # Nome della collezione delle transazioni
            'localField': 'id_utente',
            'foreignField': 'id_utente',
            'as': 'user_transactions'
        }
    },
    {
        '$project': {
            '_id': 0,
            'id_utente': 1,
            'num_transazioni': { '$size': '$user_transactions' }
        }
    }
]

    
    results = list(db[users_collection].aggregate(pipeline))
    if results:
        for result in results:
            print(f"[{percentuale}%] - Numero di transazioni dell'utente con id_utente {result['id_utente']}: {result['num_transazioni']}")
    else:
        print(f"[{percentuale}%] - Non trovato nessun utente e transazioni")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 2): {first_execution_time} ms")

    # Aggiungi il tempo di risposta medio della prima esecuzione al dizionario per la prima query
    first_response_time[f"{percentuale} - Query 2"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        results = list(db[users_collection].aggregate(pipeline))
        end_time = time.time()
        tempo_esecuzione = round((end_time - start_time) * 1000, 2)
        response_time.append(tempo_esecuzione)
    
    next_average_time = round(np.mean(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 2): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 2): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")

    average_response_time[f"{percentuale} - Query 2"] = (next_average_time, mean, margin_of_error)


# Query 3: Trova quante transazioni ha fatto l'utente Bryan Poole dall'inizio del 2023
def find_transactions_time(users_collection, transactions_collection):
    start_time = time.time()

    user_name = "Bryan Poole"  # Nome dell'utente
    start_date = '2023-01-01' #Data di inizio 

    pipeline = [
        {
            '$match': {
                'nome': user_name.split()[0],
                'cognome': user_name.split()[1]
            }
        },
        {
            '$lookup': {
                'from': transactions_collection,
                'localField': 'id_utente',
                'foreignField': 'id_utente',
                'as': 'user_transactions'
            }
        },
        {
            '$unwind': '$user_transactions'
        },
        {
            '$match': {
                'user_transactions.data': {'$gte': start_date}
            }
        },
        {
            '$group': {
                '_id': '$id_utente',
                'num_transactions': {'$sum': 1}
            }
        }
    ]

    results = list(db[users_collection].aggregate(pipeline))
    if results:
        for result in results:
            print(f"[{percentuale}%] - Numero di transazioni dall'inizio del 2023: {result['num_transactions']}")
    else:
        print(f"[{percentuale}%] - Nessuna transazione trovata per questo utente dall'inizio del 2023")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 3): {first_execution_time} ms")

    # Aggiungi il tempo di risposta medio della prima esecuzione al dizionario per la prima query
    first_response_time[f"{percentuale} - Query 3"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        results = list(db[users_collection].aggregate(pipeline))
        end_time = time.time()
        tempo_esecuzione = round((end_time - start_time) * 1000, 2)
        response_time.append(tempo_esecuzione)
    
    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 3): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 3): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")

    average_response_time[f"{percentuale} - Query 3"] = (next_average_time, mean, margin_of_error)

# Query 4: Trova con quali commercianti l'utente ha fatto almeno una transazione

def find_transactions_with_traders(users_collection, transactions_collection):
    start_time = time.time()
    user_name = "Cindy Brewer"  # Specifica il nome dell'utente di interesse

    pipeline = [
        {
            '$match': {
                'nome': user_name.split()[0],
                'cognome': user_name.split()[1]
            }
        },
        {
            '$lookup': {
                'from': transactions_collection,
                'localField': 'id_utente',
                'foreignField': 'id_utente',
                'as': 'user_transactions'
            }
        },
        {
            '$unwind': '$user_transactions'
        },
        {
            '$group': {
                '_id': '$user_transactions.id_commerciante'
            }
        },
        {
            '$lookup': {
                'from': f'commercianti_{percentuale}',  # Collection dei commercianti
                'localField': '_id',
                'foreignField': 'id',
                'as': 'merchant_info'
            }
        },
        {
            '$project': {
                '_id': 0,
                'merchant_name': '$merchant_info.commerciante'
            }
        }
    ]

    results = list(db[users_collection].aggregate(pipeline))
    if results:
        for result in results:
            print(f"[{percentuale}%] - Commerciante con cui l'utente ha effettuato transazioni: {result['merchant_name']}")
    else:
        print(f"[{percentuale}%] - Nessun commerciante trovato per questo utente")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 4): {first_execution_time} ms")

    # Aggiungi il tempo di risposta medio della prima esecuzione al dizionario per la prima query
    first_response_time[f"{percentuale} - Query 4"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        results = list(db[users_collection].aggregate(pipeline))
        end_time = time.time()
        tempo_esecuzione = round((end_time - start_time) * 1000, 2)
        response_time.append(tempo_esecuzione)
    
    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio delle 30 esecuzioni successive (Query 4): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 4): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")

    average_response_time[f"{percentuale} - Query 4"] = (next_average_time, mean, margin_of_error)

for percentuale in percentuali:

    users_collection = f'utenti_{percentuale}'
    transactions_collection = f'transazioni_{percentuale}'
    trader_collection = f'commercianti_{percentuale}'
    response_time = []  # Resetta la lista dei tempi di risposta per ogni iterazione

    find_transactions_ordered_by_amount(transactions_collection)
    find_transactions_per_user(users_collection)
    find_transactions_time(users_collection, transactions_collection)
    find_transactions_with_traders(users_collection, transactions_collection)


# Scrivo i tempi di risposta medi della prima esecuzione in un file CSV
with open('first_execution_time_mongodb.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Percentuale', 'Query', 'Millisecondi'])

    # Scrivo i dati
    for query, first_execution_time in first_response_time.items():
        dataset, query = query.split(' - ')
        writer.writerow([dataset, query, first_execution_time])

# Scrivo i tempi di risposta medi delle 30 esecuzioni successive in un file CSV
with open('average_30_executions_time_mongodb.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Percentuale', 'Query', 'Media', 'Intervallo di Confidenza (Min, Max)'])

    # Scrivo i dati
    for query, (tempo_medio_successive, mean_value, margin_of_error) in average_response_time.items():
        dataset, query = query.split(' - ')
        min_interval = round(mean_value - margin_of_error, 2)
        max_interval = round(mean_value + margin_of_error, 2)
        intervallo_di_confidenza = (min_interval, max_interval)  # Creo una tupla con minimo e massimo
        writer.writerow([dataset, query, tempo_medio_successive, intervallo_di_confidenza])

print("I file 'first_execution_time_mongodb.csv' e 'average_30_executions_time_mongodb.csv' sono stati generati correttamente.")