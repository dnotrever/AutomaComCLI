import time

from selenium_core import sc

class ServicesOrder:

    def open_services(date):

        ## Service Order
        sc.click('xpath', '/html/body/div[1]/div[3]/div/div[1]/div[30]/ul/li[1]/a')

        ## Uncheck Opens
        sc.click('xpath', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input')

        ## Uncheck Forwardeds
        sc.click('xpath', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[2]/table/tbody/tr[3]/td[1]/input')

        ## Date
        date_format = date.strftime('%d/%m/%Y')

        # test_date = '31/07/2023' ##TEST

        date1 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[1]'
        sc.click('xpath', date1)
        sc.element('xpath', date1).send_keys(date_format)

        date2 = '/html/body/div[2]/div/div[3]/table/tbody/tr/td[3]/div[3]/input[2]'
        sc.click('xpath', date2)
        sc.element('xpath', date2).send_keys(date_format)

        time.sleep(1)

        ## Filters OK
        sc.click('xpath', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[1]/input[1]')

        time.sleep(1)

        return sc.element('xpath', '/html/body/div[2]/div/div[3]/table/tbody/tr/td[5]/div[2]/span[2]').text.split(' ')

