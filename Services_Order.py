import time, re
from datetime import datetime, timedelta

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

class Services_Order:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def open_services(self, date):

        ## Service Order
        service_order = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[28]/ul/li[1]/a')))
        self.driver.execute_script('arguments[0].click();', service_order)

        ## Uncheck Opens
        opens = self.wait.until(located((By.ID, 'Status_A')))
        self.driver.execute_script('arguments[0].click();', opens)

        ## Uncheck Forwardeds
        forwardeds = self.wait.until(located((By.ID, 'Status_EN')))
        self.driver.execute_script('arguments[0].click();', forwardeds)

        ## Date
        date_format = date.strftime('%d/%m/%Y')

        # test_date = '31/07/2023' ## TEST

        date1_input = self.wait.until(located((By.ID, 'data1')))
        self.driver.execute_script('arguments[0].click();', date1_input)
        date1_input.send_keys(date_format)

        date2_input = self.wait.until(located((By.ID, 'data2')))
        self.driver.execute_script('arguments[0].click();', date2_input)
        date2_input.send_keys(date_format)

        time.sleep(1)

        ## Filters OK
        confirm_btn = self.wait.until(located((By.CSS_SELECTOR, 'input[value="OK"]')))
        self.driver.execute_script('arguments[0].click();', confirm_btn)

        time.sleep(1)

        return self.wait.until(located((By.CLASS_NAME, 'pPageStat'))).text.split(' ') # 2 4
