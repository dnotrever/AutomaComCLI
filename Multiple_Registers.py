import time, re
from datetime import datetime
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Search_Register import Search_Register
from Register_Infos import Register_Infos

class Multiple_Registers:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def format_phone(self, phone):
        phone = ''.join(re.findall('[0-9]+', phone))
        if (len(phone) > 10):
            return f'({phone[:2]}) {phone[2:7]}-{phone[7:11]}'
        elif (len(phone) > 9):
            return f'({phone[:2]}) {phone[2:6]}-{phone[6:10]}'
        else:
            return phone

    def gerenate_infos(self, name, condominium, block, apt, phone, login, band, complement, district, multiple_list):

        # phone = self.format_phone(phone)

        multiple_list.write(f'{name}\n{condominium} - {band}\n\n')

    def multiple_infos(self, df_registers):
        
        multiple_list = open('../Registers_Infos.txt', 'w', encoding='utf-8')

        condominium_list = pd.read_excel('sheets/Condominiums.xlsx', sheet_name='Condomínios')

        df_registers['Cond_Code'] = df_registers['Cond_Code'].astype(str)
        condominium_list['Cond_Code'] = condominium_list['Cond_Code'].astype(str)

        multiple_infos = pd.merge(df_registers, condominium_list, on='Cond_Code')
        multiple_infos.drop('Cond_Code', axis=1, inplace=True)

        for _, row in multiple_infos.iterrows():

            name = row['Register_Name']
            condominium = row['Condominium']
            block = str(row['Block'])
            apt = str(row['Apt'])
            phone = str(row['Phone'])
            login = row['Login']
            band = row['Band'].replace('_', ' - ')
            complement = str(row['Complement'])
            district = row['District']

            self.gerenate_infos(name, condominium, block, apt, phone, login, band, complement, district, multiple_list)
        
        multiple_list.close()

    def multiple_verify(self):

        ## Search
        registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
        self.driver.execute_script('arguments[0].click();', registers)

        registers_list = open('sheets/Multiple_List.txt', 'r', encoding='utf-8')
        
        registers = []

        for register in registers_list:

            Search_Register.open_register_search(self, 'name', register)

            data = Register_Infos(self.driver).get_register_infos('2')

            registers.append(data)

            time.sleep(1)
            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            ## Clear Name
            self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()
            
        df_registers = pd.DataFrame(registers, columns=['Register_Name', 'Cond_Code', 'Block', 'Apt', 'Complement', 'District', 'Phone', 'Login', 'Band'])

        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        self.multiple_infos(df_registers)

        return ['success', 'Successfully multiple registers infos listed.']


