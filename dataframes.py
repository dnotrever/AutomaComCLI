import pandas as pd

condominiums = pd.read_excel('sheets/Condominiums.xlsx', sheet_name='Condomínios')
customers_list = pd.read_excel("sheets/Services_Infos.xlsx")

registrations = pd.merge(customers_list, condominiums, on='Cond_Cod')
registrations.drop('Cond_Cod', axis=1, inplace=True)
