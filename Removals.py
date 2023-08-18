import time
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Search_Register import Search_Register as SEARCH
from Datetime_Now import Datetime_Now as NOW

class Removals:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def gerenate_infos(self, name, status, removal_status, removal_date, removals):

        if removal_status == 'Finalizado':
            if status == 'Ativo':
                removals.write(f'{name}  *{status}*\n')
            else:
                removals.write(f'{name}\n')

    def removals_infos(self, df_removals):

        current_date = NOW.define_datime_now()

        removals = open(f'../Removals_Infos_{current_date}.txt', 'w', encoding='utf-8')

        removals.write('*Retirados:*\n')

        for _, row in df_removals.iterrows():
        
            name = row['Register_Name']
            status = row['Status']
            removal_status = row['Removal_Status']
            removal_date = row['Removal_Date']

            self.gerenate_infos(name, status, removal_status, removal_date, removals)
        
        removals.close()

    def removals_verify(self):

        ## Search
        registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
        self.driver.execute_script('arguments[0].click();', registers)

        removals_list = open('sheets/Removals_List.txt', 'r', encoding='utf-8')

        removals = []
        
        for register in removals_list:

            removal_status = ''
            removal_date = ''

            SEARCH.open_register_search(self, 'name', register)
        
            ## Get Name
            name = self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')

            ## Login Tab
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]'))).click()

            actived = self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[2]/div/dom[2]'))).text

            # if actived == 'Sim': status = 'Ativo'

            status = 'Ativo' if actived == 'Sim' else 'Desativado'

            ## OS Tab
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[11]'))).click()

            services_list = self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[5]/table/tbody')))

            services = get_wait(services_list).until(all_located((By.TAG_NAME, 'tr')))

            first_removal = False

            for service in services:

                if first_removal: break

                subjects = get_wait(service).until(all_located((By.CSS_SELECTOR, "td[abbr='su_oss_assunto.assunto']")))

                for subject in subjects:

                    if get_wait(subject).until(located((By.TAG_NAME, 'div'))).text == 'Retirada de Equipamentos':

                        first_removal = True

                        removal_status = get_wait(service).until(located((By.CSS_SELECTOR, "td[abbr='su_oss_chamado.status']"))).text

                        if removal_status == 'Finalizado':

                            removal_date = get_wait(service).until(located((By.CSS_SELECTOR, "td[abbr='su_oss_chamado.data_fechamento']"))).text

                            break

            removals += [[name, status, removal_status, removal_date]]

            time.sleep(1)
            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            ## Clear Name
            clear_name = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')))
            self.driver.execute_script('arguments[0].click();', clear_name)

        df_removals = pd.DataFrame(removals, columns=['Register_Name', 'Status', 'Removal_Status', 'Removal_Date'])
        
        time.sleep(1)
        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        self.removals_infos(df_removals)

        return ['success', 'Successfully removals listed.']


