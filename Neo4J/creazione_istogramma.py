import pandas as pd
import matplotlib.pyplot as plt
import re

# Specifica i percorsi completi dei file CSV per MongoDB e Neo4j
mongo_csv_paths = [
    "C:\\Users\\shata\\OneDrive\\Desktop\\Development\\LINGUAGGIO_PYTHON\\Progetto_Database\\MongoDB\\first_execution_time_mongodb.csv",
    "C:\\Users\\shata\\OneDrive\\Desktop\\Development\\LINGUAGGIO_PYTHON\\Progetto_Database\\MongoDB\\average_30_executions_time_mongodb.csv",
]

neo4j_csv_paths = [
    "C:\\Users\\shata\\OneDrive\\Desktop\\Development\\LINGUAGGIO_PYTHON\\Progetto_Database\\Neo4J\\first_execution_time_neo4j.csv",
    "C:\\Users\\shata\\OneDrive\\Desktop\\Development\\LINGUAGGIO_PYTHON\\Progetto_Database\\Neo4J\\average_30_executions_time_neo4j.csv",
]

# Leggi i dati dai file CSV
first_execution_mongodb = pd.read_csv(mongo_csv_paths[0], sep=',', dtype={'Intervallo di Confidenza (Min, Max)': str})
average_30_executions_mongodb = pd.read_csv(mongo_csv_paths[1], sep=',', dtype={'Intervallo di Confidenza (Min, Max)': str})

first_execution_neo4j = pd.read_csv(neo4j_csv_paths[0], sep=',', dtype={'Intervallo di Confidenza (Min, Max)': str})
average_30_executions_neo4j = pd.read_csv(neo4j_csv_paths[1], sep=',', dtype={'Intervallo di Confidenza (Min, Max)': str})

# Lista delle dimensioni del dataset
dataset_sizes = ['25', '50', '75', '100']

# Lista delle query
queries = ['Query 1', 'Query 2', 'Query 3', 'Query 4']

# Definisce i colori per MongoDB e Neo4j
color_mongo = 'red'
color_neo4j = 'purple'

# Funzione per estrarre i valori minimi e massimi dall'intervallo di confidenza
def extract_confidence_values(confidence_interval_str):
    if isinstance(confidence_interval_str, str):
        matches = re.findall(r'\d+\.\d+', confidence_interval_str)
        return float(matches[0]), float(matches[1])
    return None, None

# Per ogni query, crea gli istogrammi
for query in queries:
    # Filtra i dati per la query corrente
    first_execution_query_mongodb = first_execution_mongodb[first_execution_mongodb['Query'] == query]
    average_30_executions_query_mongodb = average_30_executions_mongodb[average_30_executions_mongodb['Query'] == query]

    first_execution_query_neo4j = first_execution_neo4j[first_execution_neo4j['Query'] == query]
    average_30_executions_query_neo4j = average_30_executions_neo4j[average_30_executions_neo4j['Query'] == query]

    # Crea il primo istogramma con i tempi della prima esecuzione
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo_first_execution = first_execution_query_mongodb[first_execution_query_mongodb['Percentuale'] == int(size)]['Millisecondi']
        values_neo4j_first_execution = first_execution_query_neo4j[first_execution_query_neo4j['Percentuale'] == int(size)]['Millisecondi']

        plt.bar([f"{size} (MongoDB)", f"{size} (Neo4j)"], [values_mongo_first_execution.values[0], values_neo4j_first_execution.values[0]],
                color=[color_mongo, color_neo4j])

    plt.xlabel('Dimensione del Dataset')
    plt.ylabel('Tempo di esecuzione (ms)')
    plt.title(f'Istogramma - Tempo della Prima Esecuzione per {query}')
    plt.legend()
    plt.tight_layout()

    # Salva il grafico come file PNG nella cartella corrente
    filename = f'Istogramma_Tempo_Prima_Esecuzione_{query}.png'
    plt.savefig(filename)

    # Mostra il grafico
    plt.show()

    # Rimuovi il grafico dalla memoria
    plt.close()

    # Crea il secondo istogramma con le medie dei tempi
    plt.figure(figsize=(10, 6))
    for size in dataset_sizes:
        values_mongo = average_30_executions_query_mongodb[average_30_executions_query_mongodb['Percentuale'] == int(size)]['Media']
        values_neo4j = average_30_executions_query_neo4j[average_30_executions_query_neo4j['Percentuale'] == int(size)]['Media']

        # Estrae intervalli di confidenza
        confidence_intervals_mongo = average_30_executions_query_mongodb[average_30_executions_query_mongodb['Percentuale'] == int(size)][
            'Intervallo di Confidenza (Min, Max)']
        confidence_intervals_neo4j = average_30_executions_query_neo4j[average_30_executions_query_neo4j['Percentuale'] == int(size)][
            'Intervallo di Confidenza (Min, Max)']
        conf_intervals_mongo = [extract_confidence_values(conf_str) for conf_str in confidence_intervals_mongo]
        conf_intervals_neo4j = [extract_confidence_values(conf_str) for conf_str in confidence_intervals_neo4j]

        # Estrae valori minimi e massimi dagli intervalli di confidenza
        conf_mongo_min = [conf[0] for conf in conf_intervals_mongo]
        conf_mongo_max = [conf[1] for conf in conf_intervals_mongo]
        conf_neo4j_min = [conf[0] for conf in conf_intervals_neo4j]
        conf_neo4j_max = [conf[1] for conf in conf_intervals_neo4j]

        # Calcolo la differenza tra il valore medio e gli estremi dell'intervallo di confidenza
        mongo_yerr = [[values_mongo.values[0] - conf_mongo_min[0]], [conf_mongo_max[0] - values_mongo.values[0]]]
        neo4j_yerr = [[values_neo4j.values[0] - conf_neo4j_min[0]], [conf_neo4j_max[0] - values_neo4j.values[0]]]

        # Rappresenta l'intervallo di confidenza per MongoDB e Neo4j
        plt.bar(f"{size} (MongoDB)", values_mongo.values[0], yerr=mongo_yerr, capsize=5, color=color_mongo, label='MongoDB')
        plt.bar(f"{size} (Neo4j)", values_neo4j.values[0], yerr=neo4j_yerr, capsize=5, color=color_neo4j, label='Neo4j')

    plt.xlabel('Dimensione Dataset')
    plt.ylabel('Tempo medio di esecuzione (ms)')
    plt.title(f'Istogramma - Tempo di Esecuzione Medio per {query}')
    plt.legend()
    plt.tight_layout()

    # Salva il grafico come file PNG nella cartella corrente
    filename = f'Istogramma_Tempo_Esecuzione_Medio_{query}.png'
    plt.savefig(filename)

    # Mostra il grafico
    plt.show()

    # Rimuovi il grafico dalla memoria
    plt.close()