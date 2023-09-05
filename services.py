import time, re, traceback
from datetime import datetime, timedelta
import pandas as pd

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Services_Order import Services_Order
from Register_Infos import Register_Infos

class Services:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

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
        for service_type, subject_list in plan_subjects.items():
            if subject in subject_list: return service_type
            else: return 'Visita Técnica'

    def generate_services(self, subject, name, condominium, block, apt, phone, description, login, band, complement, tomorrow_date, services):

        subject = self.format_subject(subject)
        phone = self.format_phone(phone)

        if subject != 'Retirada de Equipamentos': description = re.sub(r'[\n\r]+', ' ', description) + '\n' + login + ' - ' + band
        else: description = description.split('\n')[0] 

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

            pagination = Services_Order.open_services(self, self.tomorrow_date)

            service_index = 0

            registers = []

            for _ in range(int(pagination[4])):

                time.sleep(1)

                ## Registers List
                services = self.wait.until(all_located((By.CSS_SELECTOR, 'tr[data-campoautoincrement="id"]')))

                service_index += 1

                service = services[service_index-1]

                ## Get Subject
                subject_parent = get_wait(service).until(located((By.CSS_SELECTOR, 'td[abbr="su_oss_assunto.assunto"]')))
                subject = get_wait(subject_parent).until(located((By.TAG_NAME, 'div')))

                if subject.text != 'Instalação':

                    subject = subject.text

                    get_actions(self.driver).double_click(service).perform()

                    time.sleep(1)

                    ## Get Description
                    description = self.wait.until(located((By.ID, 'mensagem'))).get_attribute('value')

                    ## Register_Infos Register
                    self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/button[3]/img'))).click()

                    data = Register_Infos(self.driver).get_register_infos('3')

                    data.append(subject)
                    data.append(description)

                    registers.append(data)

                    for _ in range(2):
                        time.sleep(1)
                        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                if service_index == int(pagination[2]) and pagination[2] != pagination[4]:
                    next_btn = self.wait.until(located((By.CSS_SELECTOR, 'i[title="Próximo"]')))
                    self.driver.execute_script('arguments[0].click();', next_btn)
                    service_index = 0
                    time.sleep(1)

            df_services = pd.DataFrame(registers, columns=['Register_Name', 'Cond_Code', 'Block', 'Apt', 'Complement', 'District', 'Phone', 'Login', 'Band', 'Subject', 'Description'])

            time.sleep(1)
            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            services_count = self.services_list(df_services)

            return ['success', ' Services listed: ' + self.info + str(services_count)]
    
        except:

            return ['error', traceback.format_exc()]

