import time

from Selenium import interaction

class Attendances:

    def __init__(self, driver):
        self.driver = driver

    def define_attendant(self, code):
        attend = {
            '0': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[11]', ## R
            '1': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[2]', ## A
        }
        return attend.get(code, None)

    def transfer(self, code):

        driver = self.driver

        ## Attedances
        interaction(driver, 'click', '/html/body/div/div[4]/div[5]')

        time.sleep(2)

        attendances = interaction(driver, 'selector_all', 'div[class="chat"]')

        for customer in attendances:

            time.sleep(1)

            interaction(driver, 'click --e', customer)

            order = customer.get_attribute('style').split('-')[1][:2]

            print(f'\n{order}')

            ## No Fixed
            if order == '16':

                ## Transfer Button 1
                interaction(driver, 'click', '/html/body/div/div[6]/div[2]/div[21]/button[2]')

                ## Support Option
                interaction(driver, 'click', '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]')

                ## Transfer Button 2
                interaction(driver, 'click', '/html/body/div[2]/div/div[2]/form/div[1]/button')

            ## Fixed
            elif order == '17':

                message = 'Estarei transferindo o atendimento para o nosso próximo atendente para darmos continuidade à sua tratativa. Nosso atendimento de Suporte Técnico Remoto agora é *24 horas*!'

                ## Message
                interaction(driver, 'send_keys', '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]', message)

                ## Send Message
                interaction(driver, 'click', '/html/body/div/div[6]/div[1]/div[3]/div[3]')

                time.sleep(1)

                ## Transfer Button 1
                interaction(driver, 'click', '/html/body/div/div[6]/div[2]/div[21]/button[2]')

                ## Support Option
                interaction(driver, 'click', '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]')

                ## Attedant
                interaction(driver, 'click', self.define_attendant(code))

                ## Transfer Button 2
                interaction(driver, 'click', '/html/body/div[2]/div/div[2]/form/div[1]/button')

                time.sleep(1)

                ## OK Button
                interaction(driver, 'click', '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')

    def message(self, main_tag, counter_tag, finish, text):

        driver = self.driver

        text = text.replace(' + ', '\n') + '\n'

        ## Attedances
        interaction(driver, 'click', '/html/body/div/div[4]/div[5]/i')

        time.sleep(2)

        attendances = interaction(driver, 'selector_all', 'div[class="chat"]')

        count = 0

        for customer in attendances:

            time.sleep(1)

            attendance_tags = customer.text.split('\n')[2]

            if main_tag in attendance_tags and counter_tag not in attendance_tags:

                count += 1

                interaction(driver, 'click', customer)

                ## Message Box
                interaction(driver, 'send_keys', '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]', text)

                if finish:

                   interaction(driver, 'click', '/html/body/div/div[6]/div[2]/div[21]/button[1]')

                   interaction(driver, 'click', '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')

        return ['success', f'Message sent to {count} customers.']

