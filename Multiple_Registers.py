import time, re, traceback
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located

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

        # multiple_list.write(f'{name}\n{condominium} - {band}\n\n')
        multiple_list.write(f'{name}\n{condominium} - Bloco {block} - Apto {apt}\n\n')

    def multiple_infos(self, df_registers):

        multiple_list = open('../Register_Infos.txt', 'a', encoding='utf-8')
        
        condominium_list = pd.read_excel('sheets/Condominiums.xlsx', sheet_name='Condomínios')

        df_registers['Cond_Code'] = df_registers['Cond_Code'].astype(str)

        condominium_list['Cond_Code'] = condominium_list['Cond_Code'].astype(str)

        multiple_infos = pd.merge(df_registers, condominium_list, on='Cond_Code')
        multiple_infos.drop('Cond_Code', axis=1, inplace=True)

        name = multiple_infos['Register_Name'][0]
        condominium = multiple_infos['Condominium'][0]
        block = str(multiple_infos['Block'][0])
        apt = str(multiple_infos['Apt'][0])
        phone = str(multiple_infos['Phone'][0])
        login = multiple_infos['Login'][0]
        band = multiple_infos['Band'][0].replace('_', ' - ')
        complement = str(multiple_infos['Complement'][0])
        district = multiple_infos['District'][0]

        self.gerenate_infos(name, condominium, block, apt, phone, login, band, complement, district, multiple_list)
        
        multiple_list.close()

    def multiple_verify(self):

        try:

            ## Search
            registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
            self.driver.execute_script('arguments[0].click();', registers)

            registers_list = open('sheets/Multiple_List.txt', 'r', encoding='utf-8')
            
            registers = []

            for register in registers_list:

                df_registers = pd.DataFrame(columns=['Register_Name', 'Cond_Code', 'Block', 'Apt', 'Complement', 'District', 'Phone', 'Login', 'Band'])

                Search_Register.open_register_search(self, 'name', register)

                data = Register_Infos(self.driver).get_register_infos('2')

                time.sleep(1)
                get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                ## Clear Name
                self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()
                
                df_registers.loc[len(df_registers)] = data

                self.multiple_infos(df_registers)

            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            return ['success', ' Successfully multiple registers infos listed.']
        
        except:
            
            return ['error', traceback.format_exc()]

