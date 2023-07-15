def transfer_attendances(op_code='0', attend='RAP', test=False):

    import time
    from access_system import By, Keys, clickable, all_located, wait, actions, open_system

    open_system(2, op_code)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def define_attend(code):
        attend = {
            'RAP': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[11]',
            'ALE': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[2]',
        }
        return attend.get(code, None)

    ## Balãozinho
    wait.until(clickable((By.XPATH, '/html/body/div/div[4]/div[5]'))).click()

    time.sleep(2)

    attendances = wait.until(all_located((By.CLASS_NAME, 'chat')))

    for customer in attendances:

        time.sleep(1)

        customer.click()

        order = customer.get_attribute('style').split('-')[1][:2]

        if order == '16':

            ## Transferir 1
            wait.until(clickable((By.CLASS_NAME, 'darken-2'))).click()

            ## Suporte
            wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]'))).click()

            if test:
                time.sleep(3)
                actions.send_keys(Keys.ESCAPE).perform()

            if not test:

                ## Transferir 2
                wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[1]/button'))).click()

        # Fixed
        elif order == '17':

            message = 'Estarei transferindo o atendimento para o nosso próximo atendente para darmos continuidade à sua tratativa. Nosso atendimento de Suporte Técnico Remoto agora é *24 horas*!'

            ## Mensagem
            wait.until(clickable((By.ID, 'input_envio_msg'))).send_keys(message)

            if not test:

                ## Enviar
                wait.until(clickable((By.XPATH, '/html/body/div/div[6]/div[1]/div[3]/div[3]'))).click()

                time.sleep(1)

            ## Transferir 1
            wait.until(clickable((By.CLASS_NAME, 'darken-2'))).click()

            ## Suporte
            wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]'))).click()

            ## Atendente
            wait.until(clickable((By.XPATH, define_attend(attend)))).click()

            if test:
                time.sleep(3)
                actions.send_keys(Keys.ESCAPE).perform()

            if not test:

                ## Transferir 2
                wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[1]/button'))).click()

                time.sleep(1)

                ## OK
                wait.until(clickable((By.CLASS_NAME, 'btn-blue'))).click()

# transfer_attendances('0', 'RAP', False)