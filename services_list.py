import time
import traceback
import re 
import pandas as pd
from datetime import datetime, timedelta
from selenium_core import sc
from services_order import ServicesOrder as Services
from register_infos import RegisterInfos as Register

from traceback_formatted import traceback_formatted

class ServicesList:

    def __init__(self):
        self.tomorrow_date = datetime.now() + timedelta(days=1)
        self.info = '\033[36m'

    def format_phone(self, phone):

        phone = ''.join(re.findall('[0-9]+', phone))

        if (len(phone) > 10):
            return f'({phone[:2]}) {phone[2:7]}-{phone[7:11]}'
        
        elif (len(phone) > 9):
            return f'({phone[:2]}) {phone[2:6]}-{phone[6:10]}'
        
        else:
            return phone

    def format_subject(self, subject):

        plan_subjects = {
            'Migração de Tecnologia': ['Migração de tecnologia e Upgrade de banda', 'Migração de Plano'],
            'Troca de Roteador': ['Upgrade de Velocidade', 'Downgrade de Velocidade', 'Troca de Roteador'],
            'Mudança de endereço': ['Mudança de Endereço'],
            'Retirada de Equipamentos': ['Retirada de Equipamentos']
        }

        subject_format = 'Visita Técnica'

        for service_type, subject_list in plan_subjects.items():
            if subject in subject_list:
                subject_format = service_type
                break

        return subject_format

    def generate_services(self, subject, name, condominium, block, apt, phone, description, login, band, complement, tomorrow_date, services):

        subject = self.format_subject(subject)
        phone = self.format_phone(phone)

        if subject != 'Retirada de Equipamentos':
            description = re.sub(r'[\n\r]+', ' ', description) + '\n' + login + ' - ' + band
        else:
            description = description.split('\n')[0] 

        services.write(f'\n*{subject} - {tomorrow_date}*\n{name}\n{condominium} - Bloco {block.zfill(2)} - Apto {apt.zfill(2)}\n{phone}\n{description}\n')

    def services_list(self, dataframe):

        condominium_list = pd.read_excel('sheets/Condominiums.xlsx', sheet_name='Condomínios')

        dataframe['Cond_Code'] = dataframe['Cond_Code'].astype(str)
        condominium_list['Cond_Code'] = condominium_list['Cond_Code'].astype(str)

        services_list = pd.merge(dataframe, condominium_list, on='Cond_Code')
        services_list.drop('Cond_Code', axis=1, inplace=True)

        services = open('../Services_List.txt', 'w')
        
        services_count = 0

        for _, row in services_list.iterrows():

            subject = row['Subject']
            name = row['Register_Name']
            condominium = row['Condominium']
            block = str(row['Block'])
            apt = str(row['Apt'])
            complement = str(row['Complement'])
            phone = str(row['Phone'])
            description = row['Description']
            login = row['Login']
            band = row['Band'].split('_')[0]

            services_day = self.tomorrow_date.day
            services_month = self.tomorrow_date.month

            tomorrow_date = str(services_day).zfill(2) + '/' + str(services_month).zfill(2)

            self.generate_services(subject, name, condominium, block, apt, phone, description, login, band, complement, tomorrow_date, services)

            services_count += 1
        
        services.close()

        return services_count

    def services_infos(self):
            
        try:

            pagination = Services.open_services(self.tomorrow_date)

            service_index = 0

            registers = []

            print('')

            for _ in range(int(pagination[4])):

                time.sleep(1)

                ## Registers List
                services = sc.element('selector', 'tr[data-campoautoincrement="id"]', 'all')

                service_index += 1

                service = services[service_index-1]

                ## Get Subject
                subject = sc.element('selector', 'td[abbr="su_oss_assunto.assunto"]', 'belongs', service)

                if not 'Instalação' in subject.text:

                    subject = subject.text

                    sc.click('none', service, 'double')

                    time.sleep(1)

                    ## Get Description
                    description = sc.element('xpath', '/html/body/form[2]/div[3]/div[1]/dl[19]/dd/textarea').get_attribute('value')

                    ## Register Edit
                    sc.click('xpath', '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/button[3]/img')

                    data = Register.get_register_infos(3)

                    data.append(subject)
                    data.append(description)

                    registers.append(data)

                    for _ in range(2):
                        sc.action('esc')

                if service_index == int(pagination[2]) and pagination[2] != pagination[4]:

                    ## Next Page Button
                    sc.click('xpath', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[1]/i[4]')

                    time.sleep(2)

                    service_index = 0

            columns = [
                'Register_Name',
                'Cond_Code',
                'Block',
                'Apt',
                'Complement',
                'District',
                'Phone',
                'Login',
                'Band',
                'Subject',
                'Description'
            ]

            df_services = pd.DataFrame(registers, columns=columns)

            # sc.action('esc')
            sc.refresh()
            sc.alert('accept')

            services_count = self.services_list(df_services)

            return ['success', ' Services listed: ' + self.info + str(services_count)]

        except:

            return ['error', traceback_formatted(traceback.format_exc())]

services = ServicesList()