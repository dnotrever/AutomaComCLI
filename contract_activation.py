import time

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

from Clear_Connection import Clear_Connection

class Contract_Activation:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def contract_activation(self):

        try:

            ## Contract Tab
            contract_tab = self.wait.until(clickable((By.XPATH, '/html/body/form/div[3]/ul/li[7]/a')))
            self.driver.execute_script('arguments[0].click();', contract_tab)

            ## Edit Contract
            self.wait.until(clickable((By.XPATH, '/html/body/form/div[3]/div[7]/dl/div/div/div[2]/div[1]/button[2]'))).click()

            ## Active
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[2]/button[5]'))).click()

            time.sleep(4)

            ## Save
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[2]/button[2]'))).click()

            time.sleep(2)

        except: pass

        get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

        Clear_Connection.clear_register_connection(self)

        return ['success', 'Successfully contract actived.']


