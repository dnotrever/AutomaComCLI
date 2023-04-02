def os_scheduling(op, test=False, secs=1.0):

    import time
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import access_system as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    backslash = "\\"

    schedulings = pd.read_excel('sheets/os_schedulings.xlsx')

    OpenAccess.I_url_access(driver, op)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Abrir Cadastro
    time.sleep(secs)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Abrir Clientes
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for _, row in schedulings.iterrows():

        columns = [
            row['Customer'],
            row['Subject'],
            row['Description'],
            row['Date'],
        ]

        customer, subject, description, date = columns

        period = row['Period'].split('-')
        
        ## Procurar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'q'))).send_keys(customer)
        time.sleep(secs)
        driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)

        time.sleep(secs)
        if driver.find_element(By.CSS_SELECTOR, f'#{backslash}31 _grid > div > div.sDiv > span.pPageStat').text != '1 - 1 / 1':
                
            ## Marcar Cliente
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[text()="{customer}"]'))).click()

        ## Editar
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'editar'))).click()

        ## Atendimento e OS Criados ?
        if subject == 0:

            ## OS
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/ul/li[11]/a'))).click()

            ## Com Descrição ?
            if type(description) != float:

                ## Editar
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]'))).click()

                ## Horário
                if period[0] >= '09:00' and period[1] <= '13:00':
                    time.sleep(secs)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#melhor_horario_agendaM'))).click()

                elif period[0] >= '13:00' and period[1] <= '18:00':
                    time.sleep(secs)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#melhor_horario_agendaT'))).click()

                ## Descrição
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).click()
                for _ in range(25): driver.find_element(By.NAME, 'mensagem').send_keys(Keys.UP)
                driver.find_element(By.NAME, 'mensagem').send_keys(Keys.HOME)
                driver.find_element(By.NAME, 'mensagem').send_keys(description)

                ## Salvar
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

                ## Fechar 2
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Ações
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/div'))).click()

            ## Agendar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]'))).click()

            ## Data e Hora Inicial
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agendamento').click()
            driver.find_element(By.NAME, 'data_agendamento').click()
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agendamento').send_keys(f'{date} {period[0]}')

            ## Data e Hora Final
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agendamento_final').click()
            driver.find_element(By.NAME, 'data_agendamento_final').click()
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agendamento_final').send_keys(f'{date} {period[1]}')

            ## Mensagem
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).send_keys('Agendado')

            ## Colaborador
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_tecnico'))).send_keys('21')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.TAB)

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[1]'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Criar Atendimento e OS ?
        else:

            ## Atendimentos
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[10]/a'))).click()

            ## Novo
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#{backslash}31 2 > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)'))).click()

            ## Assunto 1
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_assunto'))).send_keys(subject)

            ## Departamento
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_ticket_setor'))).send_keys('2')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_ticket_setor'))).send_keys(Keys.TAB)

            ## Descrição
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'menssagem'))).send_keys(description)

            ## Salvar Atendimento
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Abrir OS
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[3]/div[2]/button[5]'))).click()

            ## Assunto 2
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[4]/div[3]/div[1]/dl[5]/dd/input'))).send_keys(subject)

            ## Horário
            if period[0] >= '09:00' and period[1] <= '13:00':
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#melhor_horario_agendaM'))).click()

            elif period[0] >= '13:00' and period[1] <= '18:00':
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#melhor_horario_agendaT'))).click()

            ## Setor
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'setor'))).send_keys('1')

            ## Colaborador
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.BACKSPACE)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.BACKSPACE)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_tecnico'))).send_keys('21')

            ## Datas e Horários
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[4]/div[3]/ul/li[3]/a'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Data e Hora Inicial
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agenda').click()
            driver.find_element(By.NAME, 'data_agenda').click()
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agenda').send_keys(f'{date} {period[0]}')

            ## Data e Hora Final
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agenda_final').click()
            driver.find_element(By.NAME, 'data_agenda_final').click()
            time.sleep(secs)
            driver.find_element(By.NAME, 'data_agenda_final').send_keys(f'{date} {period[1]}')

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[4]/div[2]/button[2]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Fechar 1
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[4]/div[1]/div[3]/a[4]'))).click()

            ## Fechar 2
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Fechar 3
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

        ## Desmarcar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

    ## Logout
    time.sleep(secs)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i').click()

    driver.close()

    return 'OS registradas e agendadas com sucesso.'

# print(os_scheduling('0', True))