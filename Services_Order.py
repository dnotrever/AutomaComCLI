import time

from Selenium import get_wait, script_click, get_text, send_keys

class Services_Order:

    def __init__(self, driver):
        self.driver = driver
        self.wait = get_wait(self.driver)

    def open_services(self, date):

        ## Service Order
        script_click(self, '/html/body/div[1]/div[3]/div/div[1]/div[28]/ul/li[1]/a')

        ## Uncheck Opens
        script_click(self, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input')

        ## Uncheck Forwardeds
        script_click(self, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[1]/input')

        ## Date
        date_format = date.strftime('%d/%m/%Y')

        # test_date = '31/07/2023' ##TEST

        date1 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[1]'
        script_click(self, date1)
        send_keys(self, date1, date_format)

        date2 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[2]'
        script_click(self, date2)
        send_keys(self, date2, date_format)

        time.sleep(1)

        ## Filters OK
        script_click(self, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[1]/input[1]')

        time.sleep(1)

        return get_text(self, '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[2]').split(' ')

