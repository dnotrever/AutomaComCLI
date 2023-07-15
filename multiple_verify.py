def multiple_customers(op_code):

    import re
    import pandas as pd

    from access_system import By, Keys, clickable, wait, actions, open_system

    open_system(1, op_code)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    ## Registers
    wait.until(clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Customers
    wait.until(clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    multiple_list = open('sheets/Multiple_List.txt', 'r', encoding='utf-8')

    multiple = []

    for customer in multiple_list:

        ## Search
        wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/input'))).send_keys(customer)

        actions.send_keys(Keys.ENTER).perform()

        actions.double_click(wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[6]/table/tbody/tr[1]')))).perform()
    
        ## Get NAME
        name = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')
        
        ## Address
        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[2]'))).click()

        ## Get CONDOMINIUM
        condominium = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[2]/dl[2]/dd/input[1]'))).get_attribute('value')
        condominium = condominium if condominium else 0

        ## Get BLOCK
        block = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[2]/dl[3]/dd/input'))).get_attribute('value')
        block = re.sub('[a-zA-Z]', '', block)
        block = block if block else 0

        ## Get APTO
        apt = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[2]/dl[4]/dd/input'))).get_attribute('value')
        apt = re.sub('[a-zA-Z]', '', apt)
        apt = apt if apt else 0

        ## Get COMPLEMENT
        complement = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[2]/dl[9]/dd/input'))).get_attribute('value')
        complement = complement if complement else 0

        ## Contact
        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[3]'))).click()

        ## Get PHONE
        phone = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[3]/dl[5]/dd/input'))).get_attribute('value')
        phone = phone if phone else 0

        ## Login
        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]'))).click()

        ## Get LOGIN
        login = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div'))).text

        ## Contract
        wait.until(clickable((By.XPATH, '/html/body/form/div[3]/ul/li[7]'))).click()

        ## Get BAND
        band = wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[12]/div'))).text

        actions.send_keys(Keys.ESCAPE).perform()

        ## Clear Name
        wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

        multiple += [[name, condominium, block, apt, complement, phone, login, band]]
        
    df = pd.DataFrame(multiple, columns=['Customer', 'Cond_Cod', 'Block', 'Apt', 'Complement', 'Phone', 'Login', 'Band'])
    df.to_excel('sheets/Multiple_Infos.xlsx', index=False, header=True)

    ## Logout
    wait.until(clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i'))).click()

    multiple_list.close()

    import multiple_infos
    multiple_infos.multiple_create()

multiple_customers('0')