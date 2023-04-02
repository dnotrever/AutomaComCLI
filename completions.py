def register_ending_services():
    import dataframes
    endings = open('../customers_services.txt', 'w')
    for _, row in dataframes.total_services.iterrows():
        columns = [
            row['Cliente'],
            row['Assunto'],
        ]
        customer, subject = columns
        if subject != 'Instalação':
            endings.write(f'{customer}\n')
    endings.close()
    return 'Lista de clientes para fechamento de OS gerada.'

# print(register_ending_services())