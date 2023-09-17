import time, traceback

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located

from Search_Register import Search_Register as SEARCH

class Clear_Connection:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        self.detail = '\033[90m'

    def clear_register_connection(self):

        ## Register
        register = self.wait.until(located((By.CSS_SELECTOR, 'input[name="razao"]'))).get_attribute('value')

        ## Login Tab
        self.wait.until(clickable((By.XPATH, '/html/body/form/div[3]/ul/li[8]/a'))).click()

        ## Clear MAC
        self.wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[10]'))).click()

        alert = self.driver.switch_to.alert
        alert.accept()

        time.sleep(2)

        ## Disconnect Login
        self.wait.until(clickable((By.XPATH, f'/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[11]'))).click()

        alert = self.driver.switch_to.alert
        alert.accept()

        time.sleep(1)
        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        return register

    def search_register(self, type, register_id):

        try:

            ## Search
            registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
            self.driver.execute_script('arguments[0].click();', registers)

            SEARCH.open_register_search(self, type, register_id)

            register = self.clear_register_connection()
            
            time.sleep(1)
            get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            return ['success', ' Successfully register connection cleaned. ' + self.detail + '[ ' + register + ' ]']

        except:
            
            return ['error', traceback.format_exc()]

