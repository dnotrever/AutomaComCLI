def verify_removals(op_code):

    import pandas as pd

    from access_system import By, Keys, clickable, wait, actions, open_system, all_located
    from Selenium import get_wait

    open_system(1, op_code)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    ## Registers
    wait.until(clickable((By.XPATH, '//*[text()="Cadastros"]'))).click()

    ## Customers
    wait.until(clickable((By.XPATH, '//*[text()="Clientes"]'))).click()

    removals_list = open('sheets/Removals_List.txt', 'r', encoding='utf-8')

    removals = []
    
    for customer in removals_list:

        status = 'Desativado'
        removal_status = '-'
        removal_date = '-'

        ## Search
        wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/input'))).send_keys(customer)
        actions.send_keys(Keys.ENTER).perform()
        actions.double_click(wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[6]/table/tbody/tr[1]')))).perform()
    
        ## Get NAME
        name = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')

        ## Login
        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]'))).click()

        actived = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[2]/div/dom[2]'))).text

        if actived == 'Sim': status = 'Ativo'

        ## O.S.
        wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[11]'))).click()

        services_list = wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[11]/dl/div/div/div[5]/table/tbody')))

        services = get_wait(services_list, 30).until(all_located((By.TAG_NAME, 'tr')))

        for service in services:

            subjects = get_wait(service, 30).until(all_located((By.CSS_SELECTOR, "td[abbr='su_oss_assunto.assunto']")))

            for subject in subjects:

                if get_wait(subject, 30).until(clickable((By.TAG_NAME, 'div'))).text == 'Retirada de Equipamentos':

                    removal_status = get_wait(service, 30).until(clickable((By.CSS_SELECTOR, "td[abbr='su_oss_chamado.status']"))).text

                    if removal_status == 'Finalizado':
                        removal_date = get_wait(service, 30).until(clickable((By.CSS_SELECTOR, "td[abbr='su_oss_chamado.data_fechamento']"))).text

                    break

        # wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[8]'))).TEST

        actions.send_keys(Keys.ESCAPE).perform()

        ## Clear Name
        wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/span/i'))).click()

        removals += [[name, status, removal_status, removal_date]]
        
    df = pd.DataFrame(removals, columns=['Name', 'Status', 'Removal_Status', 'Removal_Date'])
    df.to_excel('sheets/Removals_Infos.xlsx', index=False, header=True)

    ## Logout
    wait.until(clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/i'))).click()

    removals_list.close()

    import removals_infos
    removals_infos.removals_create()

verify_removals('0')