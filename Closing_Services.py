import time
from datetime import datetime
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Services_Order import Services_Order
from Search_Register import Search_Register

class Closing_Services:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        self.today_date = datetime.now()

        self.closing_sheet = 'sheets/Closing_Services.xlsx'

    def closing_verify(self):

        pagination = Services_Order.open_services(self, self.today_date)

        service_index = 0

        registers_infos = []

        for _ in range(int(pagination[4])):

            register_id = 0

            time.sleep(1)

            ## Customers List
            services = self.wait.until(all_located((By.CSS_SELECTOR, 'tr[data-campoautoincrement="id"]')))

            service_index += 1

            service = services[service_index-1]

            status_parent = get_wait(service).until(located((By.CSS_SELECTOR, 'td[abbr="su_oss_assunto.assunto"]')))
            status = get_wait(status_parent).until(located((By.TAG_NAME, 'div')))

            if status.text != 'Instalação':

                register_name = get_wait(service).until(located((By.CSS_SELECTOR, 'td[abbr="cliente.razao"]')))
                
                get_actions(self.driver).double_click(service).perform()

                time.sleep(1)

                register_id = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')

                time.sleep(1)
                get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                registers_infos += [[int(register_id), register_name.text]]

            if service_index == int(pagination[2]) and pagination[2] != pagination[4]:
                next_btn = self.wait.until(located((By.CSS_SELECTOR, 'i[title="Próximo"]')))
                self.driver.execute_script('arguments[0].click();', next_btn)
                service_index = 0
                time.sleep(2)

        ## Dataframe

        dataframe = pd.read_excel(self.closing_sheet)

        new_registers = pd.DataFrame(registers_infos, columns=['ID', 'Customer'])

        dataframe = pd.concat([dataframe, new_registers], ignore_index=True)

        dataframe.to_excel(self.closing_sheet, index = False, header=True)

        time.sleep(1)
        for _ in range(4): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        return ['success', 'Customers with services to be closed listed!']

    def closing_execute(self):

        ## Search
        registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
        self.driver.execute_script('arguments[0].click();', registers)

        ## Dataframe
        dataframe = pd.read_excel(self.closing_sheet)

        for index, row in dataframe.iterrows():

            customer_id = row['ID']
            name = row['Customer']
            status = row['Status']
            date = row['Date']
            technician = row['Technician']
            protocol = row['Protocol']
            images = row['Images']
            description = row['Description']

            Search_Register.open_register_search(self, 'id', customer_id)

            ## OS Tab
            self.wait.until(located((By.CSS_SELECTOR, r'#\32 _form > div.abas.clearfix > ul > li:nth-child(11) > a'))).click()

            service = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[5]/table/tbody/tr[1]')))

            ## Service Status
            status_parent = get_wait(service).until(located((By.CSS_SELECTOR, 'td[abbr="su_oss_chamado.status"]')))
            status_child = get_wait(status_parent).until(located((By.TAG_NAME, 'font')))

            if status_child.text == 'Agendado' or status_child.text == 'Aberto':

                if not pd.isna(images):

                    ## Edit Service
                    edit_btn = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]')))
                    self.driver.execute_script('arguments[0].click();', edit_btn)

                    time.sleep(1)

                    images_list = images.split('\n')

                    ## File Tab
                    files_tab = self.wait.until(located((By.XPATH, '/html/body/form[3]/div[3]/ul/li[5]/a')))
                    self.driver.execute_script('arguments[0].click();', files_tab)

                    for image in images_list:

                        time.sleep(2)

                        ## New File Button
                        new_btn = self.wait.until(located((By.CSS_SELECTOR, r'#\34  > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)')))
                        self.driver.execute_script('arguments[0].click();', new_btn)

                        image_descr = image.split('_')[0].upper()

                        ## Insert Image Description
                        self.wait.until(located((By.NAME, 'descricao'))).send_keys(image_descr)

                        image_path = 'C:/Users/Everton 2/Pictures/' + image.split('_')[1]

                        ## Insert Image Path
                        self.wait.until(located((By.XPATH, '/html/body/form[4]/div[3]/div/dl[6]/dd/input[1]'))).send_keys(image_path)

                        ## Save Button
                        save_btn = self.wait.until(located((By.XPATH, '/html/body/form[4]/div[2]/button[2]')))
                        self.driver.execute_script('arguments[0].click();', save_btn)

                    time.sleep(2)

                description_format = f'{description} {technician} - Protocolo: {protocol}' if not pd.isna(protocol) else f'{description} {technician}'

                if status == 'F':
                    
                    ## Finalization Button
                    final_btn = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[9]')))
                    self.driver.execute_script('arguments[0].click();', final_btn)

                if status == 'E':

                    ## Forward Button
                    forward_btn = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[2]')))
                    self.driver.execute_script('arguments[0].click();', forward_btn)

                    time.sleep(1)

                    ## Insert Sector
                    self.wait.until(located((By.NAME, 'id_setor'))).click()
                    get_actions(self.driver).send_keys(Keys.BACKSPACE).perform()
                    self.wait.until(located((By.NAME, 'id_setor'))).send_keys('2')

                if status == 'R':

                    ## Reschedule Button
                    final_btn = self.wait.until(located((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]')))
                    self.driver.execute_script('arguments[0].click();', final_btn)

                    ## Dates
                    date1_input = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div/dl[3]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', date1_input)
                    date1_input.send_keys(date + ' 09:00:00')

                    date2_input = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div/dl[4]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', date2_input)
                    date2_input.send_keys(date + ' 18:00:00')

                    ## Collaborator
                    collaborator = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div/dl[7]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', collaborator)
                    collaborator.send_keys('21')
                    get_actions(self.driver).send_keys(Keys.TAB).perform()

                time.sleep(2)

                ## Insert Description
                descr_input = self.wait.until(located((By.NAME, 'mensagem')))
                descr_input.clear()
                descr_input.send_keys(description_format)

                time.sleep(1)

                ## Save Button
                save_btn = self.wait.until(located((By.XPATH, '/html/body/form[3]/div[2]/button[1]')))
                self.driver.execute_script('arguments[0].click();', save_btn)

            else: continue

            time.sleep(1)
            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            ## Clear Input Name
            clear_name = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')))
            self.driver.execute_script('arguments[0].click();', clear_name)

        time.sleep(1)
        for _ in range(2): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        return ['success', 'Successfully services closed!']


