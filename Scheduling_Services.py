import time, traceback
import pandas as pd

from Selenium import interaction, action

from Search_Register import Search_Register as SEARCH

from traceback_formatted import traceback_formatted

class Scheduling_Services:

    def __init__(self, driver):
        self.driver = driver
        self.scheduling_sheet = 'sheets/Scheduling_Services.xlsx'
    
    def scheduling_verify(self):

        driver = self.driver

        try:

            ## Attendances
            interaction(driver, 'click', '/html/body/div/div[4]/div[5]/i')

            attend_list = interaction(driver, 'selector', 'div[class="list_dados"]')

            attend_body = interaction(attend_list, 'selector_all', 'div[class="corpo"]')

            services = []

            for attendance in attend_body:

                time.sleep(1)

                customer_name = attendance.text.split('\n')[0]
                tags = attendance.text.split('\n')[2]

                if 'Agendar Visita' in tags:

                    interaction(driver, 'click', attendance)

                    customer_id = interaction(driver, 'text', '/html/body/div/div[6]/div[2]/div[4]/span')

                    notes = interaction(driver, 'text', '/html/body/div/div[6]/div[2]/div[12]/div/div[2]/div[1]').split(' # ')

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
            
            return ['error', traceback_formatted(traceback.format_exc())]

    def scheduling_execute(self):

        driver = self.driver
            
        try:

            ## Search
            interaction(driver, 'click', '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')

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
                    interaction(driver, 'click', '/html/body/form[2]/div[3]/ul/li[11]/a')

                    ## Description?
                    if not pd.isna(description):

                        ## Edit
                        interaction(driver, 'click', '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]')

                        time.sleep(1)

                        ## Description
                        message = '/html/body/form[3]/div[3]/div[1]/dl[28]/dd/textarea'
                        interaction(driver, 'click', message)
                        for _ in range(15): action(driver, 'up')
                        interaction(driver, 'click', message, description)

                        time.sleep(2)

                        ## Save
                        interaction(driver, 'click', '/html/body/form[2]/div[2]/button[2]')

                        action(driver, 'esc')

                    time.sleep(2)

                    ## Actions
                    actions_btn = interaction(driver, 'click', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/div/span')

                    time.sleep(1)

                    ## Schedule Button
                    interaction(driver, 'click', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]')

                    ## Dates
                    date1 = '/html/body/form[3]/div[3]/div/dl[3]/dd/input'
                    interaction(driver, 'click', date1)
                    interaction(driver, 'send_keys', date1, date + ' 09:00:00')

                    date2 = '/html/body/form[3]/div[3]/div/dl[4]/dd/input'
                    interaction(driver, 'click', date2)
                    interaction(driver, 'send_keys', date2, date + ' 18:00:00')

                    ## Message
                    interaction(driver, 'send_keys', '/html/body/form[3]/div[3]/div/dl[6]/dd/textarea', 'Agendado.')

                    ## Collaborator
                    interaction(driver, 'send_keys', '/html/body/form[3]/div[3]/div/dl[7]/dd/input', '21')

                    action(driver, 'tab')

                    time.sleep(1)

                    ## Save
                    interaction(driver, 'selector', r'#\33 _form > div.tDiv > button:nth-child(1)')
                    
                ## Create Service and OS
                else:

                    ## Service Tab
                    interaction(driver, 'click', '/html/body/form[2]/div[3]/ul/li[10]/a')

                    time.sleep(2)

                    ## New Service #--> CORRIGIR: ele pega o botão de criar novo cliente 
                    interaction(driver, 'click --e', interaction(driver, 'selector', 'button[name="novo"]'))

                    time.sleep(1)

                    ## Subject
                    interaction(driver, 'send_keys', '/html/body/form[3]/div[3]/div[1]/dl[10]/dd/input', subject)

                    ## Department
                    interaction(driver, 'send_keys', '/html/body/form[3]/div[3]/div[1]/dl[18]/dd/input[1]', '2')

                    action(driver, 'tab')

                    ## Description
                    interaction(driver, 'send_keys', '/html/body/form[3]/div[3]/div[1]/dl[28]/dd/textarea', description)

                    time.sleep(2)

                    ## Save Service
                    interaction(driver, 'click', '/html/body/form[3]/div[2]/button[2]')

                    time.sleep(2)

                    ## OS Tab
                    interaction(driver, 'click', '/html/body/form[3]/div[2]/button[5]')

                    time.sleep(2)

                    ## Sector
                    interaction(driver, 'send_keys', '/html/body/form[4]/div[3]/div[1]/dl[17]/dd/input', '1')

                    ## Collaborator
                    interaction(driver, 'clear', '/html/body/form[4]/div[3]/div[1]/dl[18]/dd/input')
                    interaction(driver, 'send_keys', '/html/body/form[4]/div[3]/div[1]/dl[18]/dd/input', '21')

                    time.sleep(1)

                    ## DateTimes
                    interaction(driver, 'click', '/html/body/form[4]/div[3]/ul/li[3]/a')

                    time.sleep(1)

                    ## Initial DateTime
                    interaction(driver, 'click', '/html/body/form[4]/div[3]/div[3]/dl[4]/dd/input')
                    interaction(driver, 'send_keys', '/html/body/form[4]/div[3]/div[3]/dl[4]/dd/input', f'{date} {period[0]}:00')

                    time.sleep(2)

                    ## Final DateTime
                    interaction(driver, 'click', '/html/body/form[4]/div[3]/div[3]/dl[5]/dd/input')
                    interaction(driver, 'send_keys', '/html/body/form[4]/div[3]/div[3]/dl[5]/dd/input', f'{date} {period[1]}:00')

                    time.sleep(1)

                    ## Save OS
                    interaction(driver, 'click', '/html/body/form[4]/div[2]/button[2]')

                    time.sleep(2)

                    for _ in range(2):
                        action(driver, 'esc')

                action(driver, 'esc')

                ## Clear Input Name
                clear = interaction(driver, 'selector', r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')
                interaction(driver, 'click', clear)

            action(driver, 'esc')

            return ['success', ' Successfully services scheduled!']
    
        except:
                
            return ['error', traceback_formatted(traceback.format_exc())]

