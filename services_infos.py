def services_infos(op_code, date):

    import re
    import pandas as pd

    from access_system import By, Keys, clickable, wait, actions, open_system

    open_system(1, op_code)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    ## Suporte
    wait.until(clickable((By.XPATH, '//*[text()="Suporte"]'))).click()

    ## Ordem de Serviço
    wait.until(clickable((By.XPATH, '//*[text()="Ordem de Serviço"]'))).click()

    ## Abertos
    wait.until(clickable((By.NAME, 'Status_A'))).click()

    ## Encaminhados
    wait.until(clickable((By.NAME, 'Status_EN'))).click()

    ## Data Inicial
    wait.until(clickable((By.NAME, 'data1'))).click()
    wait.until(clickable((By.NAME, 'data1'))).send_keys(date)

    ## Data Final
    wait.until(clickable((By.NAME, 'data2'))).click()
    wait.until(clickable((By.NAME, 'data2'))).send_keys(date)

    ## Filtro
    wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[1]/input[1]'))).click()

    ## Quantity
    qty = wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[2]'))).text
    qty_format = re.sub('[-/]', '', qty)
    qty_arr = [x for x in qty_format.split(' ') if x != '']

    customers = []
    factor = 1
    paginate = False

    for num in range(1, int(qty_arr[2])+1):

        if num > int(qty_arr[1]):
    
            wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[1]/i[4]'))).click()
            paginate = True

        if paginate:
            num = factor
            factor += 1

        service = wait.until(clickable((By.XPATH, f'/html/body/div[2]/div/div[6]/table/tbody/tr[{num}]')))

        subject = wait.until(clickable((By.XPATH, f'/html/body/div[2]/div/div[6]/table/tbody/tr[{num}]/td[10]/div'))).text
        
        if subject != 'Instalação':

            name = condominium = block = apt = complement = district = phone = login = band = description = ''

            ## Service
            actions.double_click(service).perform()

            ## Get DESCRIPTION
            description = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[19]/dd/textarea'))).get_attribute("value")

            ## Register
    
            wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/button[3]/img'))).click()

            ## Get NAME
            name = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[1]/dl[2]/dd/input'))).get_attribute("value")
            
            ## Address
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/ul/li[2]/a'))).click()

            ## Get CONDOMINIUM
            condominium = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[2]/dl[2]/dd/input[1]'))).get_attribute("value")
            condominium = condominium if condominium != '' else 0

            ## Get BLOCK
            block = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[2]/dl[3]/dd/input'))).get_attribute("value")
            block = re.sub('[a-zA-Z]', '', block)
            block = block if block else 0

            ## Get APTO
            apt = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[2]/dl[4]/dd/input'))).get_attribute("value")
            apt = re.sub('[a-zA-Z]', '', apt)
            apt = apt if apt else 0

            ## Get COMPLEMENT
            complement = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[2]/dl[9]/dd/input'))).get_attribute("value")
            complement = complement if complement else 0

            ## Get DISTRICT
            district = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[2]/dl[10]/dd/input'))).get_attribute("value")
            district = district if district != '0' else 0

            ## Contact
    
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/ul/li[3]'))).click()

            ## Get PHONE
            phone = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[3]/dl[5]/dd/input'))).get_attribute("value")
            phone = phone if phone else 0

            ## Login
            wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/ul/li[8]'))).click()

            ## Get LOGIN
            login = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div'))).text

            ## Get BAND
            band = wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[6]/div'))).text

            customers += [[name, condominium, block, apt, complement, district, phone, login, band, subject, description]]

            for _ in range(2): actions.send_keys(Keys.ESCAPE).perform()

        else: continue

    df = pd.DataFrame(customers, columns=['Customer', 'Cond_Cod', 'Block', 'Apt', 'Complement', 'District', 'Phone', 'Login', 'Band', 'Subject', 'Description'])
    df.to_excel('sheets/Services_Infos.xlsx', index = False, header=True)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    ## Logout
    wait.until(clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i'))).click()

    return f'(data: {date})'

# print(services_infos('0', '03/04/2023'))