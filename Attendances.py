import pandas as pd
import time, re
from datetime import datetime, timedelta

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

class Attendances:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def define_attendant(self, code):
        attend = {
            '0': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[11]', # RAP
            '1': '/html/body/div[2]/div/div[2]/form/div[2]/div[3]/select/option[2]', # ALE
        }
        return attend.get(code, None)

    def transfer(self, code):

        ## Attedances
        self.wait.until(clickable((By.XPATH, '/html/body/div/div[4]/div[5]'))).click()

        time.sleep(2)

        attendances = self.wait.until(all_located((By.CLASS_NAME, 'chat')))

        for customer in attendances:

            time.sleep(1)

            customer.click()

            order = customer.get_attribute('style').split('-')[1][:2]

            ## No Fixed
            if order == '16':

                ## Transfer Button 1
                self.wait.until(clickable((By.CLASS_NAME, 'darken-2'))).click()

                ## Support Option
                self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]'))).click()

                ## Transfer Button 2
                self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[1]/button'))).click()

            ## Fixed
            elif order == '17':

                message = 'Estarei transferindo o atendimento para o nosso próximo atendente para darmos continuidade à sua tratativa. Nosso atendimento de Suporte Técnico Remoto agora é *24 horas*!'

                ## Message
                self.wait.until(clickable((By.ID, 'input_envio_msg'))).send_keys(message)

                ## Send Message
                self.wait.until(clickable((By.XPATH, '/html/body/div/div[6]/div[1]/div[3]/div[3]'))).click()

                time.sleep(1)

                ## Transfer Button 1
                self.wait.until(clickable((By.CLASS_NAME, 'darken-2'))).click()

                ## Support Option
                self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/div[2]/select/option[7]'))).click()

                ## Attedant
                self.wait.until(clickable((By.XPATH, self.define_attendant(code)))).click()

                ## Transfer Button 2
                self.wait.until(clickable((By.XPATH, '/html/body/div[2]/div/div[2]/form/div[1]/button'))).click()

                time.sleep(1)

                ## OK Button
                self.wait.until(clickable((By.CLASS_NAME, 'btn-blue'))).click()


