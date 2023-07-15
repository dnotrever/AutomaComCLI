def register_schedulings(op_code='0'):

    import time
    import pandas as pd

    from access_system import By, clickable, located, all_located, wait, open_system

    open_system(2, op_code)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    customers = []

    ## Balãozinho
    wait.until(clickable((By.XPATH, '/html/body/div/div[4]/div[5]'))).click()

    time.sleep(2)

    attendances = wait.until(all_located((By.CLASS_NAME, 'chat')))
    
    for customer in attendances:

        infos_arr = customer.text.split('\n')

        if 'Agendar Visita' in infos_arr[2]:

            name = infos_arr[0]

            customer.click()
            
            for code in ['0', '4', '16', '17', '19', '25', '38']:
                if code in infos_arr[2]: subject = code

            details = wait.until(located((By.CLASS_NAME, 'observacao_mensagem'))).text.split(' ')
            
            date = details[0]

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

            customers += [[name, subject, date, period, init_desc]]

    df = pd.DataFrame(customers, columns=['Customer', 'Subject', 'Date', 'Period', 'Description'])
    df.to_excel('sheets/OS_Schedulings.xlsx', index = False, header=True)

# print(register_schedulings('0'))