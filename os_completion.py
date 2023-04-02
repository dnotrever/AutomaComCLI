def os_completion(op, test=False, secs=1.0):

    import time
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import access_system as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    OpenAccess.I_url_access(driver, op)

    ## Abrir Cadastro
    time.sleep(secs)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Abrir Cliente
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Clientes"]'))).click()
    
    backslash = "\\"

    services = pd.read_excel('sheets/os_completions.xlsx')

    for _, row in services.iterrows():

        columns = [
            row['Customer'],
            str(row['Resolution']),
            str(row['Technician']),
            str(row['Files']),
            row['Action'],
        ]

        customer, resolution, technician, files, action = columns

        ## Reagendou ?
        if action == 'R': continue
        
        pics = files.split('\n')

        ## Procurar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'q'))).send_keys(customer)
        time.sleep(secs)
        driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)

        ## Mais de 1 Cliente ?
        time.sleep(secs)
        if driver.find_element(By.CSS_SELECTOR, f'#{backslash}31 _grid > div > div.sDiv > span.pPageStat').text == '1 - 2 / 2':
                
            ## Marcar Cliente
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[text()="{customer}"]'))).click()

        ## Editar
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'editar'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## OS
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/ul/li[11]/a'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Com Imagens
        if files != 'nan':

            ## Editar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/button[3]'))).click()
            
            for x in range(len(pics)):

                ## Arquivos
                time.sleep(secs*2)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[3]/div[3]/ul/li[5]'))).click()

                ## Novo
                time.sleep(secs*2)
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl/div/div/div[2]/div[1]/button[1]'))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#{backslash}34  > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)'))).click()

                pic_desc = pics[x].split('_')[1]
                
                ## Descrição Arquivo
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'descricao'))).send_keys(pic_desc)

                pic_path = f'C:/Users/Everton 2/Pictures/'
                pic_name = pics[x].split('_')[0]

                upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[4]/div[3]/div/dl[6]/dd/input[1]')))
                upload.send_keys(pic_path + pic_name)

                ## Salvar
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[4]/div[2]/button[2]'))).click()

            ## Fechar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

        # # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Ações
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/div'))).click()

        if technician == 'nan':
            msg = f'{resolution}'
        else:
            msg = f'{resolution} {technician}'

        if action == 'A':

            ## Reabrir
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[8]'))).click()

            msg = f'{resolution}'

            ## Mensagem
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).send_keys(msg)

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[1]'))).click()

        if action == 'F':

            ## Finalizar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[9]'))).click()

            time.sleep(secs)
            if WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).text:

                time.sleep(2)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).click()
                for _ in range(50): driver.find_element(By.NAME, 'mensagem').send_keys(Keys.BACKSPACE)

            ## Mensagem
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).send_keys(msg)

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[1]'))).click()

        if 'E' in action:

            ## Encaminhar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[11]/dl/div/div/div[2]/div[1]/nav[3]/ul/li[2]'))).click()

            ## Setor
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_setor'))).send_keys(Keys.BACK_SPACE)
            
            if action == 'E2':
                
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_setor'))).send_keys('2')

                ## Mensagem
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).send_keys(f'{msg}  Por favor, realizar cobrança.')
                
            if action == 'E8':
            
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'id_setor'))).send_keys('8')

                ## Mensagem
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'mensagem'))).send_keys(msg)

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[1]TEST'))).click()

        ## Fechar 2
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## Desmarcar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

    ## Logout
    time.sleep(secs)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i').click()

    driver.close()

    return 'OS finalizadas com sucesso.'

# print(os_completion('0', True))