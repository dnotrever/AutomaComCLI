def register_customers_schedulings(secs=0.8):

    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import access_system as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    
    OpenAccess.O_url_access(driver)

    attendances = []
    schedulings = open('../customers_schedulings.txt', 'w')

    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//html/body/div/div[4]/div[5]'))).click()

    time.sleep(secs)
    attendances = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'chat')))

    for customer in attendances:

        infos_arr = customer.text.split('\n')

        if 'Agendar Visita' in infos_arr[2]:

            customer.click()

            details = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'observacao_mensagem'))).text.split(' ')
            
            name = infos_arr[0]
            subject = ''
            init_desc = ''
            date = details[0]
            period = ''

            if '0' in infos_arr[2]:
                subject = '0'
            elif '4' in infos_arr[2]:
                subject = '4'
            elif '16' in infos_arr[2]:
                subject = '16'
            elif '17' in infos_arr[2]:
                subject = '17'
            elif '19' in infos_arr[2]:
                subject = '19'
            elif '38' in infos_arr[2]:
                subject = '38'
            elif '34' in infos_arr[2]:
                subject = '34'
            elif '25' in infos_arr[2]:
                subject = '25'

            if len(details) == 2:
                
                if '-' in details[1]:

                    time_period = details[1].split('-')

                    if time_period[0] >= '09:00' and time_period[1] <= '13:00':
                        init_desc = f'*Manhã, entre {time_period[0]} e {time_period[1]}* '

                    elif time_period[0] >= '13:00' and time_period[1] <= '18:00':
                        init_desc = f'*Tarde, entre {time_period[0]} e {time_period[1]}* '

                    else:
                        init_desc = f'*Entre {time_period[0]} e {time_period[1]}* '

                    period = details[1]

                else:

                    if details[1] == 'M':
                        init_desc = '*Manhã* '
                        period = '09:00-13:00'

                    elif details[1] == 'T':
                        init_desc = '*Tarde* '
                        period = '13:00-18:00'

                    elif details[1] == 'MT':
                        period = '09:00-18:00'
            
            elif len(details) == 3:

                condit = details[1]
                time_period = details[2]
                
                init_desc = f'*{condit} {time_period}* '

                if condit == 'Até':
                    period = f'09:00-{time_period}'

                elif condit == 'Após':
                    period = f'{time_period}-18:00'
            
            infos = f'{name}\t{subject}\t{init_desc}\t{date}\t{period}\n'

            schedulings.write(infos)
            
    schedulings.close()

    return 'Lista de clientes para agendamentos gerada.'

# print(register_customers_schedulings())