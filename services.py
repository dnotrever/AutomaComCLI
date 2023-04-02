import dataframes
import date_config as Date
import format_address as Address
import format_phone as Phone
import plan_subjects as Subjs
import re

def generate_services(subject, name, condominium, block, apt, phone, description, login, band, complement, tomorrow_date, services):

    if subject in Subjs.PlanSubjects['migration']:
        services.write('\n*Migração para Fibra - ')
    elif subject in Subjs.PlanSubjects['equip_change']:
        services.write('\n*Troca do Roteador - ')
    elif subject == 'Retirada de Equipamentos':
        services.write('\n*Retirada de Equipamento - ')
    else:
        services.write('\n*Visita Técnica - ')

    address = Address.format_address(block, apt, condominium, complement)
    phone_format = Phone.format_phone(phone)

    services.write(f'{tomorrow_date}*\n{name}\n{address}\n{phone_format}\n')

    if subject != 'Retirada de Equipamentos':
        description = re.sub(r'[\n\r]+', ' ', description)
        services.write('{}\n{} - {}\n'.format(description, login, band))
    else:
        first_row = (description.split('\n'))[0]
        services.write('{}\n'.format(first_row))

def services_infos():

    services = open('../Lista_Chamados.txt', 'w')
    
    cont = 0

    for _, row in dataframes.registrations.iterrows():

        subject = row['Subject']
        name = row['Customer']
        condominium = row['Condominium']
        block = str(row['Block'])
        apt = str(row['Apt'])
        phone = str(row['Phone'])
        description = row['Description']
        login = row['Login']
        band = row['Band'].split('_')[0]
        complement = str(row['Complement'])
        tomorrow_date = f'{Date.tomorrow_day}/{Date.tomorrow_month}'

        generate_services(subject, name, condominium, block, apt, phone, description, login, band, complement, tomorrow_date, services)

        cont += 1
    
    services.close()

    return f'{cont} chamados gerados'

# print(services_infos())