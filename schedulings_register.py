def scheduling(op_code):

    import pandas as pd

    from access_system import By, clickable, located, all_located, wait, open_system

    open_system(1, op_code)

    schedulings = pd.read_excel('sheets/Schedulings_Infos.xlsx')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Registers
    wait.until(clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Customers
    wait.until(clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for _, row in schedulings.iterrows():

        customer = row['Customer']
        subject = row['Subject']
        date = row['Date']
        description = row['Description']
        period = row['Period'].split('-')
    
        ## Cliente
        wait.until(clickable((By.NAME, 'q'))).send_keys(customer)

        driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)

        if driver.find_element(By.CSS_SELECTOR, f'#{backslash}31 _grid > div > div.sDiv > span.pPageStat').text != '1 - 1 / 1':
                
            ## Marcar Cliente
    
            wait.until(clickable((By.XPATH, f'//*[text()="{customer}"]'))).click()

        ## Editar

        wait.until(clickable((By.NAME, 'editar'))).click()

        ## Atendimento e OS Criados ?
        if subject == 0:

            ## OS
    
            wait.until(clickable((By.XPATH, '/html/body/form/div[3]/ul/li[11]/a'))).click()

            ## Com Descrição ?
            if type(description) != float:

                ## Editar
        
                wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]'))).click()

                ## Horário
                if period[0] >= '09:00' and period[1] <= '13:00':
            
                    wait.until(clickable((By.CSS_SELECTOR, '#melhor_horario_agendaM'))).click()

                elif period[0] >= '13:00' and period[1] <= '18:00':
            
                    wait.until(clickable((By.CSS_SELECTOR, '#melhor_horario_agendaT'))).click()

                ## Descrição
        
                wait.until(clickable((By.NAME, 'mensagem'))).click()
                for _ in range(25): driver.find_element(By.NAME, 'mensagem').send_keys(Keys.UP)
                driver.find_element(By.NAME, 'mensagem').send_keys(Keys.HOME)
                driver.find_element(By.NAME, 'mensagem').send_keys(description)

                ## Salvar
        
                wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

                ## Fechar 2
        
                wait.until(clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Ações
    
            wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/div'))).click()

            ## Agendar
    
            wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[4]'))).click()

            ## Data e Hora Inicial
    
            driver.find_element(By.NAME, 'data_agendamento').click()
            driver.find_element(By.NAME, 'data_agendamento').click()
    
            driver.find_element(By.NAME, 'data_agendamento').send_keys(f'{date} {period[0]}')

            ## Data e Hora Final
    
            driver.find_element(By.NAME, 'data_agendamento_final').click()
            driver.find_element(By.NAME, 'data_agendamento_final').click()
    
            driver.find_element(By.NAME, 'data_agendamento_final').send_keys(f'{date} {period[1]}')

            ## Mensagem
    
            wait.until(clickable((By.NAME, 'mensagem'))).send_keys('Agendado')

            ## Colaborador
    
            wait.until(clickable((By.NAME, 'id_tecnico'))).send_keys('21')
            wait.until(clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.TAB)

            ## Salvar
    
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[1]'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Criar Atendimento e OS ?
        else:

            ## Atendimentos
    
            wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[10]/a'))).click()

            ## Novo
    
            wait.until(clickable((By.CSS_SELECTOR, f'#{backslash}31 2 > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)'))).click()

            ## Assunto 1
    
            wait.until(clickable((By.NAME, 'id_assunto'))).send_keys(subject)

            ## Departamento
    
            wait.until(clickable((By.NAME, 'id_ticket_setor'))).send_keys('2')
            wait.until(clickable((By.NAME, 'id_ticket_setor'))).send_keys(Keys.TAB)

            ## Descrição
    
            wait.until(clickable((By.NAME, 'menssagem'))).send_keys(description)

            ## Salvar Atendimento
    
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Abrir OS
    
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form[3]/div[2]/button[5]'))).click()

            ## Assunto 2
    
            wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/div[1]/dl[5]/dd/input'))).send_keys(subject)

            ## Horário
            if period[0] >= '09:00' and period[1] <= '13:00':
        
                wait.until(clickable((By.CSS_SELECTOR, '#melhor_horario_agendaM'))).click()

            elif period[0] >= '13:00' and period[1] <= '18:00':
        
                wait.until(clickable((By.CSS_SELECTOR, '#melhor_horario_agendaT'))).click()

            ## Setor
    
            wait.until(clickable((By.NAME, 'setor'))).send_keys('1')

            ## Colaborador
    
            wait.until(clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.BACKSPACE)
            wait.until(clickable((By.NAME, 'id_tecnico'))).send_keys(Keys.BACKSPACE)
            wait.until(clickable((By.NAME, 'id_tecnico'))).send_keys('21')

            ## Datas e Horários
    
            wait.until(clickable((By.XPATH, '/html/body/form[4]/div[3]/ul/li[3]/a'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Data e Hora Inicial
    
            driver.find_element(By.NAME, 'data_agenda').click()
            driver.find_element(By.NAME, 'data_agenda').click()
    
            driver.find_element(By.NAME, 'data_agenda').send_keys(f'{date} {period[0]}')

            ## Data e Hora Final
    
            driver.find_element(By.NAME, 'data_agenda_final').click()
            driver.find_element(By.NAME, 'data_agenda_final').click()
    
            driver.find_element(By.NAME, 'data_agenda_final').send_keys(f'{date} {period[1]}')

            ## Salvar
    
            wait.until(clickable((By.XPATH, '/html/body/form[4]/div[2]/button[2]'))).click()

            # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            ## Fechar 1
    
            wait.until(clickable((By.XPATH, '/html/body/form[4]/div[1]/div[3]/a[4]'))).click()

            ## Fechar 2
    
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Fechar 3

        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

        ## Desmarcar Cliente

        wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

    ## Logout
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i').click()

    driver.close()

    return 'OS registradas e agendadas com sucesso.'

# print(scheduling('0'))