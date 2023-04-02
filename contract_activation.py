def contract_activation(op, customer_id, customer_name, test=False, secs=1.0):

    import time
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    if not test: import access_system as OpenAccess
    else: import access_system as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    backslash = "\\"

    OpenAccess.I_url_access(driver, op)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Abrir Cadastro
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Abrir Cliente
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    ## Filtro
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/span[1]'))).click()

    ## Selecionar ID
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/nav/ul/li[2]'))).click()

    ## Procurar Cliente
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'q'))).send_keys(customer_id)
    time.sleep(secs)
    driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)

    # customer_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[6]/table/tbody/tr/td[4]/div'))).text

    ## Editar
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'editar'))).click()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Contrato
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[7]/a'))).click()

    ## Editar
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/button[2]'))).click()

    ## Ativar
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[5]'))).click()

    ## Salvar
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

    ## Fechar
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[3]/div[1]/div[3]/a[4]'))).click()

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Login
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]'))).click()

    ## Limpar MAC
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[10]'))).click()
    time.sleep(secs*2)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    ## Desconectar Login
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[11]'))).click()
    time.sleep(secs*2)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## Fechar 1
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[2]/div[1]/div[3]/a[4]'))).click()

    ## Logout
    time.sleep(secs)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i').click()

    driver.close()

    return f'{customer_name} - contrato ativado.'

# print(contract_activation('0', '8950', 'Fulano', True))