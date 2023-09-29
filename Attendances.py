import time
from selenium_core import sc

class Attendances:

    def define_attendant(self, code):
        attend = {
            '0': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[11]', ## R
            '1': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[2]', ## A
        }
        return attend.get(code, None)

    def transfer(self, code):

        ## Attedances
        sc.click('xpath', '/html/body/div/div[4]/div[5]')

        time.sleep(2)

        attendances = sc.element('selector', 'div[class="chat"]', 'all')

        for customer in attendances:

            time.sleep(1)

            sc.click('none', customer)

            order = customer.get_attribute('style').split('-')[1][:2]

            ## No Fixed
            if order == '16':

                ## Transfer Button 1
                sc.click('xpath', '/html/body/div/div[6]/div[2]/div[21]/button[2]')

                time.sleep(1)

                ## Support Option
                sc.element('xpath', '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]').click()

                ## Transfer Button 2
                sc.click('xpath', '/html/body/div[2]/div/div[2]/form/div[1]/button')

            ## Fixed
            elif order == '17':

                message = 'Estarei transferindo o atendimento para o nosso próximo atendente para darmos continuidade à sua tratativa. Nosso atendimento de Suporte Técnico Remoto agora é *24 horas*!'

                ## Message
                sc.element('xpath', '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]', message).send_keys(message)

                ## Send Message
                sc.click('xpath', '/html/body/div/div[6]/div[1]/div[3]/div[3]')

                time.sleep(1)

                ## Transfer Button 1
                sc.click('xpath', '/html/body/div/div[6]/div[2]/div[21]/button[2]')

                ## Support Option
                sc.click('xpath', '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]')

                ## Attedant
                sc.click('xpath', self.define_attendant(code))

                ## Transfer Button 2
                sc.click('xpath', '/html/body/div[2]/div/div[2]/form/div[1]/button')

                time.sleep(1)

                ## OK Button
                sc.click('xpath', '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')

    def message(self, main_tag, counter_tag, finish, text):

        text = text.replace(' + ', '\n') + '\n'

        ## Attedances
        sc.click('xpath', '/html/body/div/div[4]/div[5]/i')

        time.sleep(2)

        attendances = sc.element('selector', 'div[class="chat"]', 'all')

        count = 0

        for customer in attendances:

            time.sleep(1)

            attendance_tags = customer.text.split('\n')[2]

            if main_tag in attendance_tags and counter_tag not in attendance_tags:

                count += 1

                sc.click('none', customer)

                ## Message Box
                sc.element('xpath', '/html/body/div/div[6]/div[1]/div[3]/div[1]/div[2]').send_keys(text)

                if finish:

                   sc.click('xpath', '/html/body/div/div[6]/div[2]/div[21]/button[1]')

                   sc.click('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')

        return ['success', f'Message sent to {count} customers.']

