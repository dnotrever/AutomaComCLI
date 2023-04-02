def generlized_attendance(secs=1.0, message=True, close=True):

    import time
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import access_system as OpenAccess

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    OpenAccess.O_url_access(driver)
    
    attendances = []

    message_text = 'Por falta de interação, estaremos encerrando este atendimento.  Mas se voltar a apresentar instabilidades e/ou necessitar de qualquer outra verificação, só nos chamar aqui novamente e será um prazer atender!  Tenha uma ótima noite!'
    
    time.sleep(secs)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//html/body/div/div[4]/div[5]'))).click()

    time.sleep(secs)
    attendances = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'chat')))

    for customer in attendances:

        infos_arr = customer.text.split('\n')

        if 'Rompimento' in infos_arr[2]:

            customer.click()

            if message:

                ## Mensagem
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]'))).send_keys(message_text)

                ## Enviar
                time.sleep(secs)
                driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]').send_keys(Keys.ENTER)

            if close:

                ## Encerrar
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[6]/div[2]/div[20]/button[1]'))).click()

                ## OK
                time.sleep(secs)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]'))).click()

generlized_attendance()