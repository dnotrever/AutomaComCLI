import dataframes
import date_config as Date
import format_address as Address
import format_phone as Phone

def generate_emergency(option, name, condominium, block, apt, complement, phone, login, band, current_date):

    emergency = open(f'../chamado__{name}.txt', 'w')

    if option == 't':
        emergency.write('*Visita Técnica - ')
    elif option == 'r':
        emergency.write('*Retirada de Equipamentos - ')

    address = Address.format_address(block, apt, condominium, complement)
    phone_format = Phone.format_phone(phone)

    emergency.write(f'{current_date}*\n{name}\n{address}\n{phone_format}\n')

    if option == 't':
        emergency.write('Cliente sem conexão. Los piscando vermelho e Pon pagada na Onu. \n{} - {}\n'.format(login, band))
    elif option == 'r':
        emergency.write('Retirar ')

    emergency.close()

def customer_infos(option):

    customer_infos = dataframes.infos

    for _, row in customer_infos.iterrows():

        name = row['Customer']
        condominium = row['Condominium']
        block = str(row['Block'])
        apt = str(row['Apt'])
        complement = str(row['Complement'])
        phone = str(row['Phone'])
        login = row['Login']
        band = row['Band'].split('_')[0]
        current_date = f'{Date.current_day}/{Date.current_month}'

        generate_emergency(option, name, condominium, block, apt, complement, phone, login, band, current_date)
        
        subject = 'conexão' if option == 't' else 'retirada'

        customer_name = name

        break

    return f'Chamado de {subject} gerado para {customer_name}'

# print(generate_emergency('c'))