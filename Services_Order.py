import time

from Selenium import interaction

class Services_Order:

    def open_services(driver, date):

        ## Service Order
        interaction(driver, 'click', '/html/body/div[1]/div[3]/div/div[1]/div[28]/ul/li[1]/a')

        ## Uncheck Opens
        interaction(driver, 'click', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input')

        ## Uncheck Forwardeds
        interaction(driver, 'click', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[1]/input')

        ## Date
        date_format = date.strftime('%d/%m/%Y')

        # test_date = '31/07/2023' ##TEST

        date1 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[1]'
        interaction(driver, 'click', date1)
        interaction(driver, 'send_keys', date1, date_format)

        date2 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[2]'
        interaction(driver, 'click', date2)
        interaction(driver, 'send_keys', date2, date_format)

        time.sleep(1)

        ## Filters OK
        interaction(driver, 'click', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[1]/input[1]')

        time.sleep(1)

        return interaction(driver, 'text', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[2]').split(' ')

