import time
import traceback
import os
import pandas as pd
from datetime import datetime
from selenium_core import sc

from services_order import ServicesOrder as Services
from search_register import SearchRegister as Search

class ClosingServices:

    def __init__(self):
        self.today_date = datetime.now()
        self.closing_sheet = 'sheets/Closing_Services.xlsx'
        self.directory = r'C:\Users\Everton 2\Pictures'

    def closing_verify(self, date):

        try:

            select_date = self.today_date if date == 'today' else datetime.strptime(date, "%d/%m/%Y")

            pagination = Services.open_services(select_date)

            service_index = 0

            registers_infos = []

            for _ in range(int(pagination[4])):

                register_id = 0

                time.sleep(2)

                ## Customers List
                services = sc.element('selector', 'tr[data-campoautoincrement="id"]', 'all')

                service_index += 1

                service = services[service_index-1]

                status = sc.element('selector', 'td[abbr="su_oss_assunto.assunto"]', 'belongs', service)

                if status.text != 'Instalação':

                    register_name = sc.element('selector', 'td[abbr="cliente.razao"]', 'belongs', service)
                    
                    sc.click('none', service, 'double')

                    time.sleep(2)

                    register_id = sc.element('xpath', '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input').get_attribute('value')

                    sc.action('esc')

                    registers_infos += [[int(register_id), register_name.text]]

                if service_index == int(pagination[2]) and pagination[2] != pagination[4]:
                    sc.click('selector', 'i[title="Próximo"]')
                    service_index = 0
                    time.sleep(2)

            ## Dataframe

            dataframe = pd.read_excel(self.closing_sheet)

            new_registers = pd.DataFrame(registers_infos, columns=['ID', 'Customer'])

            dataframe = pd.concat([dataframe, new_registers], ignore_index=True)

            dataframe.to_excel(self.closing_sheet, index = False, header=True)

            # sc.refresh()
            # sc.alert('accept')

            return ['success', ' Customers with services to be closed listed!']

        except:
            
            return ['error', traceback.format_exc()]

    def closing_execute(self):

        try:

            ## Search
            sc.click('xpath', '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')

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

                Search.open_register_search(self, 'id', customer_id)

                ## OS Tab
                sc.click('selector', r'#\32 _form > div.abas.clearfix > ul > li:nth-child(11) > a')

                service = sc.element('xpath', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[5]/table/tbody/tr[1]')

                ## Service Status
                status_infos = sc.element('selector', 'td[abbr="su_oss_chamado.status"]', 'belongs', service)

                if status_infos.text == 'Agendado' or status_infos.text == 'Aberto':

                    if images:

                        ## Edit Service
                        sc.click('xpath', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]')

                        time.sleep(1)

                        ## File Tab
                        sc.click('xpath', '/html/body/form[3]/div[3]/ul/li[5]/a')

                        for file in os.listdir(self.directory):

                            image_path = os.path.join(self.directory, file)

                            file = file.split('_')

                            if os.path.isfile(image_path) and len(file) > 1 and name == file[0]:
                                
                                image_descr = (file[1].split('.')[0]).upper()

                                time.sleep(2)

                                ## New File Button
                                sc.click('selector', r'#\34  > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)')

                                ## Insert Image Description
                                sc.element('name', 'descricao').send_keys(image_descr)

                                ## Insert Image Path
                                sc.element('xpath', '/html/body/form[4]/div[3]/div/dl[6]/dd/input[1]').send_keys(image_path)

                                ## Save Button
                                sc.click('xpath', '/html/body/form[4]/div[2]/button[2]')

                        sc.action('esc')

                        time.sleep(2)

                    description_format = f'{description} {technician} - Protocolo: {protocol}' if not pd.isna(protocol) else f'{description} {technician}'

                    # ## Actions
                    # sc.click('xpath', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]')

                    if status == 'F':
                        
                        ## Finalization Button
                        sc.click('xpath', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[9]')

                    if status == 'E':

                        ## Forward Button
                        sc.click('xpath', '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[2]')

                        time.sleep(1)

                        ## Insert Sector
                        sector_id = sc.element('name', 'id_setor')
                        sc.click('nome', sector_id)
                        sc.action('backspace')
                        sc.element('name', 'id_setor').send_keys('2')

                    if status == 'R':

                        ## Reschedule Button
                        sc.click('xpath', '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]')

                        ## Dates
                        date1_input = sc.element('xpath', '/html/body/form[2]/div[3]/div/dl[3]/dd/input')
                        sc.click('none', date1_input)
                        date1_input.send_keys(date + ' 09:00:00')

                        date2_input = sc.element('xpath', '/html/body/form[2]/div[3]/div/dl[4]/dd/input')
                        sc.click('none', date2_input)
                        date2_input.send_keys(date + ' 18:00:00')

                        ## Collaborator
                        collaborator = sc.click('xpath', '/html/body/form[2]/div[3]/div/dl[7]/dd/input')
                        collaborator.send_keys('21')
                        sc.action('tab')

                    time.sleep(2)

                    ## Insert Description
                    descr_input = sc.element('name', 'mensagem')
                    descr_input.clear()
                    descr_input.send_keys(description_format)

                    time.sleep(1)

                    ## Save Button
                    sc.click('xpath', '/html/body/form[3]/div[2]/button[1]')

                else: continue

                sc.action('esc')

                ## Clear Input Name
                sc.click('selector', r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')

            # sc.refresh()
            # sc.alert('accept')

            return ['success', ' Successfully services closed!']

        except:

            return ['error', traceback.format_exc()]

