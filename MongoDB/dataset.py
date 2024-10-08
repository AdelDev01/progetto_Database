from faker import Faker
import random
import csv

fake = Faker()

total_user = 10000

percentuali = [25, 50, 75, 100]

generated_user_ids = []
generated_commerce_ids = []
generated_credit_number = {}


for percentuale in percentuali:
    num_operations = 0
    num_records = int(total_user * (percentuale / 100))

    # Genera il file CSV degli utenti
    users_csv_filename = f'utenti_{percentuale}.csv'
    with open(users_csv_filename, mode='w', newline='', encoding='utf-8') as user_csvname:
        fieldnames_users = ['id_utente', 'nome', 'cognome', 'indirizzo','numero_carta']
        writer_users = csv.DictWriter(user_csvname, fieldnames=fieldnames_users)
        writer_users.writeheader()

        for num_opr in range(int(num_records / 10)):
            num_operations += 1
            credit_number = fake.credit_card_number()
            user = {
                'id_utente': num_operations,
                'nome': fake.first_name(),
                'cognome': fake.last_name(),
                'indirizzo': fake.address(),
                'numero_carta': credit_number
            }
            writer_users.writerow(user)
            generated_user_ids.append(num_operations)
            generated_credit_number[credit_number] = num_operations




        # Genera il file CSV delle informazioni sui commercianti o categorie
    commercianti_csv_filename = f'commercianti_{percentuale}.csv'
    with open(commercianti_csv_filename, mode='w', newline='', encoding='utf-8') as commercianti_csv:
        fieldnames_commercianti = ['id_commerciante','commerciante', 'categoria']
        writer_commercianti = csv.DictWriter(commercianti_csv, fieldnames=fieldnames_commercianti)
        writer_commercianti.writeheader()
        
        num_operations = 0
        for num in range(int(num_records / 50)):  
            num_operations += 1
            commerciante = {
                'id': num_operations,
                'commerciante': fake.company(),
                'categoria': fake.random_element(elements=('Abbigliamento', 'Alimentari', 'Elettronica', 'Viaggi'))
            }
            writer_commercianti.writerow(commerciante)
            generated_commerce_ids.append(num_operations)


    # Genera il file CSV delle transazioni degli utenti
    transactions_csv_filename = f'transazioni_{percentuale}.csv'
    with open(transactions_csv_filename, mode='w', newline='', encoding='utf-8') as transactions_csv:
        fieldnames_transactions = ['id_utente','id_commerciante','id_transazione', 'numero_carta', 'data', 'importo']
        transaction_writer = csv.DictWriter(transactions_csv, fieldnames=fieldnames_transactions)
        transaction_writer.writeheader()
        
        num_operations = 0
        for transaction_num in range(num_records):
            credit_number = random.choice(list(generated_credit_number.keys()))
            user_id = generated_credit_number[credit_number]
            commerce_id = random.choice(generated_commerce_ids)
            num_operations += 1
            transaction = {
                'id_utente': user_id,
                'id_commerciante': commerce_id,
                'id_transazione':num_operations,
                'numero_carta': credit_number,
                'data': fake.date_time_this_year(),
                'importo': round(random.uniform(10, 3000), 2)
                
            }
            transaction_writer.writerow(transaction)

    print(f"File CSV utenti, transazioni e informazioni commercianti {percentuale}% generati.")