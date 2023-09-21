import time, traceback

from SeleniumCore import interaction, action

from Search_Register import Search_Register as SEARCH

from traceback_formatted import traceback_formatted

class Clear_Connection:

    def __init__(self, driver):
        self.driver = driver
        self.detail = '\033[90m'

    def clear_register_connection(self, driver):

        ## Register
        register_name = interaction(driver, 'value', '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input')

        ## Login Tab
        interaction(driver, 'click', '/html/body/form/div[3]/ul/li[8]/a')

        ## Clear MAC
        interaction(driver, 'click', '/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[10]')

        alert = driver.switch_to.alert
        alert.accept()

        time.sleep(2)

        ## Disconnect Login
        interaction(driver, 'click', f'/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[11]')

        alert = driver.switch_to.alert
        alert.accept()

        action(driver, 'esc')

        return register_name

    def search_register(self, type, register_id):

        driver = self.driver

        try:

            ## Search
            interaction(driver, 'click', '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')

            SEARCH.open_register_search(self, type, register_id)

            register = self.clear_register_connection(driver)
            
            action(driver, 'esc')

            return ['success', ' Successfully register connection cleaned. ' + self.detail + '[ ' + register + ' ]']

        except:
            
            return ['error', traceback_formatted(traceback.format_exc())]

