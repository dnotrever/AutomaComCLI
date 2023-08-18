def register_logins(op, test=False, secs=1.0):

    import time, os
    import pandas as pd
    import CONF as CONF
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    if not test: import Systems as OpenAccess
    else: import Systems as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    logins_sheet = pd.read_excel('sheets/new_logins_list.xlsx')
    logins_list = open('../new_logins_list.txt', 'w')

    backslash = "\\"

    logins_list.write('*Bom dia a todos!*\nSeguem os usuários das Instalações:\n')

    OpenAccess.I_url_access(driver, op)

    ## Abrir Cadastro
    time.sleep(secs)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Abrir Clientes
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    for _, row in logins_sheet.iterrows():

        columns = [
            row['Customer'],
            row['Login'],
            row['User']
        ]

        customer, login, user = columns
        
        ## Procurar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'q'))).send_keys(customer)
        time.sleep(secs)
        driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)

        time.sleep(secs)
        if driver.find_element(By.CSS_SELECTOR, f'#{backslash}31 _grid > div > div.sDiv > span.pPageStat').text == '1 - 2 / 2':
                
            ## Marcar Cliente
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[text()="{customer}"]'))).click()

        ## Editar
        time.sleep(secs)
        driver.find_element(By.NAME, 'editar').click()

        ## Logins
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]/a'))).click()

        time.sleep(secs*4)
        if driver.find_element(By.CSS_SELECTOR, f'#{backslash}31 0 > dl > div > div > div.tDiv.bg2 > div.tDiv2 > span.pPageStat').text == '0 itens':

            ## Novo
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#{backslash}31 0 > dl > div > div > div.tDiv.bg2 > div.tDiv2 > button:nth-child(1)'))).click()

            ## Contrato
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[7]/dd/button[1]'))).click()

            ## Selecionar Contrato
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div/div[2]/div[1]/button[8]'))).click()

            ## Plano
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[10]/dd/button[2]'))).click()

            ## Atualizar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div/div[3]/span[1]/i[3]'))).click()

            ## Selecionar Plano
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div/div[2]/div[1]/button[2]'))).click()

            ## Login
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'login'))).send_keys(login)

            ## Senha
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[14]/dd/input'))).send_keys('123456')

            ## Concentrador
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[3]/ul/li[4]/a'))).click()

            ## Selecionar Concentrador
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[3]/div[3]/div[4]/dl[2]/dd/input[1]'))).send_keys('17')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[3]/div[3]/div[4]/dl[2]/dd/input[1]'))).send_keys(Keys.TAB)

            ## Salvar
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

            ## Fechar Login
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

            ## Fechar Cliente
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

            logins_list.write('\n{}\n{}\n{}\n'.format(customer, login, user))

        else:

            ## Capturar Login
            time.sleep(secs*2)
            existing_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div'))).text

            logins_list.write('\n{}\n{}\n{}\n'.format(customer, existing_login, user))

            ## Fechar Cliente
            time.sleep(secs)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

        ## Desmarcar Cliente
        time.sleep(secs)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

    ppp_pass = CONF.PPP_PASS
    app_pass = CONF.APP_PASS

    logins_list.write('\nSenha padrão PPPoE: {}\nSenha padrão do App: {}'.format(ppp_pass, app_pass))
    logins_list.close()

    ## Logout
    time.sleep(secs)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i').click()

    driver.close()

    return 'Logins cadastrados com sucesso.'

# print(register_logins('0', True))