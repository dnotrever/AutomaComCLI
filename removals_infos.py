import pandas as pd

def gerenate_infos(name, status, removal_status, removal_date, removals):

    if removal_status == 'Finalizado':
        if status == 'Ativo':
            removals.write(f'{name}  *{status}*\n')
        else:
            removals.write(f'{name}\n')

def removals_create():

    removals = open('../Removals.txt', 'w', encoding='utf-8')

    removals.write('*Retirados:*\n')

    removal_infos = pd.read_excel('sheets/Removals_Infos.xlsx')
    
    for _, row in removal_infos.iterrows():
    
        name = row['Name']
        status = row['Status']
        removal_status = row['Removal_Status']
        removal_date = row['Removal_Date']

        gerenate_infos(name, status, removal_status, removal_date, removals)
    
    removals.close()

    return f'Finished!'

# print(removals_create())