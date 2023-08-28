import time, traceback
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Search_Register import Search_Register as SEARCH

class Scheduling_Services:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        self.scheduling_sheet = 'sheets/Scheduling_Services.xlsx'
    
    def scheduling_verify(self):

        try:

            ## Attendances
            attend_btn = self.wait.until(located((By.XPATH, '/html/body/div/div[4]/div[5]/i')))
            self.driver.execute_script('arguments[0].click();', attend_btn)

            attend_list = self.wait.until(located((By.CLASS_NAME, 'list_dados')))

            attend_body = get_wait(attend_list).until(all_located((By.CLASS_NAME, 'corpo')))

            services = []

            for attendance in attend_body:

                time.sleep(1)

                customer_name = attendance.text.split('\n')[0]
                tags = attendance.text.split('\n')[2]

                if 'Agendar Visita' in tags:

                    self.driver.execute_script('arguments[0].click();', attendance)

                    customer_id = self.wait.until(located((By.XPATH, '/html/body/div/div[6]/div[2]/div[4]/span'))).text

                    notes = self.wait.until(located((By.CLASS_NAME, 'observacao_mensagem'))).text.split(' # ')

                    subject = notes[0]
                    date = notes[1]
                    period = notes[2]

                    hours = period.split('-')

                    if hours[0] == '09:00' and hours[1] < '18:00':
                        description = f'*Até às {hours[1]}* '

                    if hours[0] > '09:00' and hours[1] == '18:00':
                        description = f'*Após às {hours[0]}* '

                    if hours[0] == '09:00' and hours[1] == '13:00':
                        description = '*Manhã* '

                    if hours[0] == '13:00' and hours[1] == '18:00':
                        description = '*Tarde* '

                    if hours[0] == '09:00' and hours[1] == '18:00':
                        description = ''

                    data = [int(customer_id), customer_name , int(subject), date, period, description]

                    services.append(data)

            df_services = pd.DataFrame(services, columns=['ID', 'Customer', 'Subject', 'Date', 'Period', 'Description'])

            df_services.to_excel(self.scheduling_sheet, index = False, header=True)

            return ['success', ' Customers with services to be schedule listed!']

        except:
            
            return ['error', traceback.format_exc()]

    def scheduling_execute(self):
            
        try:

            ## Search
            registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
            self.driver.execute_script('arguments[0].click();', registers)

            schedulings = pd.read_excel(self.scheduling_sheet)

            for _, row in schedulings.iterrows():

                customer_id = row['ID']
                name = row['Customer']
                subject = row['Subject']
                date = row['Date']
                period = row['Period'].split('-')
                description = row['Description']

                SEARCH.open_register_search(self, 'id', customer_id)
        
                ## Service and OS created
                if subject == 0:

                    ## OS
                    self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/ul/li[11]/a'))).click()

                    ## Description?
                    if not pd.isna(description):

                        ## Edit
                        self.wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]'))).click()

                        time.sleep(1)

                        ## Description
                        self.wait.until(clickable((By.CSS_SELECTOR, '#mensagem'))).click()
                        for _ in range(30): get_actions(self.driver).send_keys(Keys.UP).perform()
                        self.wait.until(clickable((By.CSS_SELECTOR, '#mensagem'))).send_keys(description)

                        ## Save
                        # self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[2]/button[2]'))).click()
                        self.wait.until(clickable((By.CSS_SELECTOR, r'#\33 _form > div.tDiv > button:nth-child(2)'))).click()

                        time.sleep(1)
                        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                    time.sleep(2)

                    ## Actions
                    actions_btn = self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/div/span')))
                    self.driver.execute_script('arguments[0].click();', actions_btn)

                    time.sleep(1)

                    ## Schedule Button
                    self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]'))).click()

                    ## Dates
                    date1_input = self.wait.until(located((By.XPATH, '/html/body/form[3]/div[3]/div/dl[3]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', date1_input)
                    date1_input.send_keys(date + ' 09:00:00')

                    date2_input = self.wait.until(located((By.XPATH, '/html/body/form[3]/div[3]/div/dl[4]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', date2_input)
                    date2_input.send_keys(date + ' 18:00:00')

                    ## Message
                    self.wait.until(located((By.XPATH, '/html/body/form[3]/div[3]/div/dl[6]/dd/textarea'))).send_keys('Agendado.')

                    ## Collaborator
                    collaborator = self.wait.until(located((By.XPATH, '/html/body/form[3]/div[3]/div/dl[7]/dd/input')))
                    self.driver.execute_script('arguments[0].click();', collaborator)
                    collaborator.send_keys('21')

                    time.sleep(1)
                    get_actions(self.driver).send_keys(Keys.TAB).perform()

                    time.sleep(1)

                    ## Save
                    self.wait.until(clickable((By.CSS_SELECTOR, r'#\33 _form > div.tDiv > button:nth-child(1)'))).click()
                    
                ## Create Service and OS
                else:

                    ## Service Tab
                    self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[10]/a'))).click()

                    ## New Service
                    self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[10]/dl/div/div/div[3]/div[1]/button[1]'))).click()

                    ## Subject
                    self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[10]/dd/input'))).send_keys(subject)

                    ## Department
                    self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[18]/dd/input[1]'))).send_keys('2')

                    time.sleep(1)
                    get_actions(self.driver).send_keys(Keys.TAB).perform()

                    ## Description
                    self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[28]/dd/textarea'))).send_keys(description)

                    time.sleep(2)

                    ## Save Service
                    self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

                    time.sleep(2)

                    ## OS Tab
                    self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[5]'))).click()

                    time.sleep(2)

                    ## Sector
                    self.wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/div[1]/dl[17]/dd/input'))).send_keys('1')

                    ## Collaborator
                    self.wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/div[1]/dl[18]/dd/input'))).clear()
                    self.wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/div[1]/dl[18]/dd/input'))).send_keys('21')

                    ## DateTimes
                    self.wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/ul/li[3]/a'))).click()

                    time.sleep(1)

                    ## Initial DateTime
                    self.driver.find_element(By.XPATH, '/html/body/form[4]/div[3]/div[3]/dl[4]/dd/input').click()
                    self.driver.find_element(By.XPATH, '/html/body/form[4]/div[3]/div[3]/dl[4]/dd/input').send_keys(f'{date} {period[0]}:00')

                    time.sleep(1)

                    ## Final DateTime
                    self.driver.find_element(By.XPATH, '/html/body/form[4]/div[3]/div[3]/dl[5]/dd/input').click()
                    self.driver.find_element(By.XPATH, '/html/body/form[4]/div[3]/div[3]/dl[5]/dd/input').send_keys(f'{date} {period[1]}:00')

                    time.sleep(1)

                    ## Save OS
                    self.wait.until(clickable((By.XPATH, '/html/body/form[4]/div[2]/button[2]'))).click()

                    for _ in range(2): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                time.sleep(1)
                get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                ## Clear Input Name
                clear_name = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')))
                self.driver.execute_script('arguments[0].click();', clear_name)

            time.sleep(1)
            for _ in range(4): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            return ['success', ' Successfully services scheduled!']
    
        except:
                
            return ['error', traceback.format_exc()]

