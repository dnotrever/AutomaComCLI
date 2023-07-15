import format_address as Address
import format_phone as Phone
import pandas as pd

def gerenate_infos(name, condominium, block, apt, phone, login, band, complement, multiple):

    # address = Address.format_address(block, apt, condominium, complement)
    # phone = Phone.format_phone(phone)

    multiple.write(f'{name}\n{condominium} - {band}\n\n')

def multiple_create():

    multiple = open('../Multiple.txt', 'w', encoding='utf-8')

    condominiums = pd.read_excel('sheets/Condominiums.xlsx', sheet_name='Condomínios')
    multiple_infos = pd.read_excel('sheets/Multiple_Infos.xlsx')

    infos = pd.merge(multiple_infos, condominiums, on='Cond_Cod')
    infos.drop('Cond_Cod', axis=1, inplace=True)

    for _, row in infos.iterrows():

        name = row['Customer']
        condominium = row['Condominium']
        block = str(row['Block'])
        apt = str(row['Apt'])
        band = row['Band'].replace('_', ' - ')
        phone = str(row['Phone'])
        login = row['Login']
        complement = str(row['Complement'])

        gerenate_infos(name, condominium, block, apt, phone, login, band, complement, multiple)
    
    multiple.close()

    return f'Finished!'

# print(multiple_create())