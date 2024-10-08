import csv
import time
import numpy as np
import pandas as pd
from scipy import stats
from py2neo import Graph



def calculate_confidence_interval(data):
    confidence = 0.95
    n = len(data)
    mean_value = np.mean(data)
    stderr = stats.sem(data)
    margin_of_error = stderr * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean_value, margin_of_error


db100 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db100")
db75 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db75")
db50 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db50")
db25 = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name="db25")

percentuali = [25,50,75,100]
first_response_time = {}
average_response_time = {}
response_time = []


# Query 1: Ordina tutte le transazioni in ordine crescente

def find_transactions_ordered_by_amount(percentuale):

    start_time = time.time()

    graph = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name=f"db{percentuale}")
    pipeline = graph.run("MATCH (t:Transazione) WHERE t.importo >= 1500 AND t.importo <= 2500 RETURN t.importo ORDER BY t.importo ASC")
    results = list(pipeline)

    if results:
        for result in results:
            print(result)  # Stampa le transazioni ordinate per importo crescente
    else:
        print("Nessuna transazione trovata")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 1): {first_execution_time} ms")
    first_response_time[f"{percentuale} - Query 1"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        result = graph.run("MATCH (t:Transazione) WHERE t.importo >= 1500 AND t.importo <= 2500 RETURN t ORDER BY t.importo ASC")
        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000, 2)
        response_time.append(execution_time)

    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 1): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 1): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")
    average_response_time[f"{percentuale} - Query 1"] = (next_average_time, mean, margin_of_error)


# Query 2: Trova il numero di transazioni dell'utente Kevin Sanders
    
def find_transactions_per_user(percentuale):

    start_time = time.time()

    graph = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name=f"db{percentuale}")
    pipeline = graph.run("MATCH (u:Utente {nome: 'Kevin', cognome: 'Sanders'})-[:HA_EFFETTUATO]->(t:Transazione) RETURN u.id_utente as id_utente, COUNT(t) as num_transazioni")
    results = list(pipeline)
    if results:
        for result in results:
            print(f"Trovato id utente {result['id_utente']} e numero transazioni: {result['num_transazioni']}")  # Stampa le transazioni ordinate per importo crescente
    else:
        print("Nessuna transazione trovata")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 2): {first_execution_time} ms")
    first_response_time[f"{percentuale} - Query 2"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        result = graph.run("MATCH (u:Utente {nome: 'Kevin', cognome: 'Sanders'})-[:HA_EFFETTUATO]->(t:Transazione) RETURN u.id_utente as id_utente, COUNT(t) as num_transazioni")
        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000, 2)
        response_time.append(execution_time)

    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 2): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 2): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")
    average_response_time[f"{percentuale} - Query 2"] = (next_average_time, mean, margin_of_error)

# Query 3: Trova tutte le transazioni effettuate dall'utente Bryan Poole dall'inizio dell'anno 2023

def find_transactions_time(percentuale):

    start_time = time.time()

    graph = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name=f"db{percentuale}")
    pipeline = graph.run("MATCH (u:Utente {nome: 'Bryan', cognome: 'Poole'})-[:HA_EFFETTUATO]->(t:Transazione) WHERE t.data >= '2023-01-01' WITH u.id_utente as id_utente, COUNT(t) as num_transactions RETURN id_utente, num_transactions")
    results = list(pipeline)
    if results:
        for result in results:
            print(f"[{percentuale}%] - Numero di transazioni dall'inizio del 2023: {result['num_transactions']}")  # Stampa le transazioni ordinate per importo crescente
    else:
        print("Nessuna transazione trovata")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 3): {first_execution_time} ms")
    first_response_time[f"{percentuale} - Query 3"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()

        result = graph.run("MATCH (u:Utente {nome: 'Bryan', cognome: 'Poole'})-[:HA_EFFETTUATO]->(t:Transazione) WHERE t.data >= '2023-01-01' WITH u.id_utente as id_utente, COUNT(t) as num_transactions RETURN id_utente, num_transactions")

        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000, 2)
        response_time.append(execution_time)

    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 3): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 3): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")
    average_response_time[f"{percentuale} - Query 3"] = (next_average_time, mean, margin_of_error)

    # Query 4: Trova i commercianti con cui l'utente Cindy Brewer ha effettuato almeno una transazione

# Query 4: Trova tutti i commercianti con cui l'utente Cindy Brewer ha fatto almeno una transazione

def find_transactions_with_traders(percentuale):

    start_time = time.time()

    graph = Graph("bolt://localhost:7687", user="neo4j", password="12345678", name=f"db{percentuale}")
    pipeline = graph.run("MATCH (u:Utente {nome: 'Cindy', cognome: 'Brewer'})-[:HA_EFFETTUATO]->(t:Transazione) WITH DISTINCT t.id_commerciante AS id_commerciante MATCH (c:Commerciante {id: id_commerciante}) RETURN c.commerciante AS merchant_name")
    results = list(pipeline)
    if results:
        for result in results:
            print(f"[{percentuale}%] - Commerciante con cui l'utente ha effettuato transazioni: {result['merchant_name']}")  # Stampa le transazioni ordinate per importo crescente
    else:
        print("Nessuna transazione trovata")

    end_time = time.time()

    first_execution_time = round((end_time - start_time) * 1000, 2)
    print(f"[{percentuale}%] - Tempo di risposta (prima esecuzione - Query 4): {first_execution_time} ms")
    first_response_time[f"{percentuale} - Query 4"] = first_execution_time

    # Tempo di risposta delle successive 30 query
    for _ in range(30):
        start_time = time.time()
        result = graph.run("MATCH (u:Utente {nome: 'Cindy', cognome: 'Brewer'})-[:HA_EFFETTUATO]->(t:Transazione) WITH DISTINCT t.id_commerciante AS id_commerciante MATCH (c:Commerciante {id: id_commerciante}) RETURN c.commerciante AS merchant_name")
        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000, 2)
        response_time.append(execution_time)

    next_average_time = round(sum(response_time) / len(response_time), 2)
    mean, margin_of_error = calculate_confidence_interval(response_time)
    print(f"[{percentuale}%] - Tempo medio di 30 esecuzioni successive (Query 4): {next_average_time} ms")
    print(f"[{percentuale}%] - Intervallo di Confidenza (Query 4): [{round(mean - margin_of_error, 2)}, {round(mean + margin_of_error, 2)}] ms\n")
    average_response_time[f"{percentuale} - Query 4"] = (next_average_time, mean, margin_of_error)


for percentuale in percentuali:
    find_transactions_ordered_by_amount(percentuale)
    find_transactions_per_user(percentuale)
    find_transactions_time(percentuale)
    find_transactions_with_traders(percentuale)

# Scrivo i tempi di risposta medi della prima esecuzione in un file CSV
with open('first_execution_time_neo4j.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Percentuale', 'Query', 'Millisecondi'])

    # Scrivo i dati
    for query, first_execution_time in first_response_time.items():
        dataset, query = query.split(' - ')
        writer.writerow([dataset, query, first_execution_time])

# Scrivo i tempi di risposta medi delle 30 esecuzioni successive in un file CSV
with open('average_30_executions_time_neo4j.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Percentuale', 'Query', 'Media', 'Intervallo di Confidenza (Min, Max)'])

    # Scrivo i dati
    for query, (tempo_medio_successive, mean_value, margin_of_error) in average_response_time.items():
        dataset, query = query.split(' - ')
        min_interval = round(mean_value - margin_of_error, 2)
        max_interval = round(mean_value + margin_of_error, 2)
        intervallo_di_confidenza = (min_interval, max_interval)  # Creo una tupla con minimo e massimo
        writer.writerow([dataset, query, round(mean_value, 2), intervallo_di_confidenza])

print("I file 'first_execution_time_neo4j.csv' e 'average_30_executions_time_neo4j.csv' sono stati generati correttamente.")
