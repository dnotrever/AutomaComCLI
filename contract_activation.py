import time

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located

from Clear_Connection import Clear_Connection as CLEAR

class Contract_Activation:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        self.detail = '\033[90m'

    def contract_activation(self):

        try:

            ## Register
            register = self.wait.until(located((By.CSS_SELECTOR, 'input[name="razao"]'))).get_attribute('value')

            ## Contract Tab
            contract_tab = self.wait.until(located((By.CSS_SELECTOR, 'a[rel="7"]')))
            self.driver.execute_script('arguments[0].click();', contract_tab)

            ## Status
            status = self.wait.until(located((By.CSS_SELECTOR, 'td[abbr="cliente_contrato.status_internet"]')))

            if 'Desativado' in status.text:

                time.sleep(1)

                ## Edit Contract
                edit_contract = self.wait.until(located((By.CSS_SELECTOR, 'button[name="editar"]')))
                self.driver.execute_script('arguments[0].click();', edit_contract)

                time.sleep(1)

                ## Active
                active_btn = self.wait.until(clickable((By.CSS_SELECTOR, 'button[id="ativar_outro"]')))
                self.driver.execute_script('arguments[0].click();', active_btn)

                time.sleep(4)

                ## Save
                save_btn = self.wait.until(clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
                self.driver.execute_script('arguments[0].click();', save_btn)

                time.sleep(2)

                get_actions(self.driver).send_keys(Keys.ESCAPE).perform()
                
            CLEAR.clear_register_connection(self)

            return ['success', ' Successfully contract actived! ' + self.detail + '[ ' + register + ' ]']

        except:
            
            return ['error', traceback.format_exc()]

