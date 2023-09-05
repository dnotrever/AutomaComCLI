import time, traceback

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located

from Search_Register import Search_Register as SEARCH
from Set_DateTime import Set_DateTime as DATETIME
from Clear_Connection import Clear_Connection as CLEAR

class Unlock_Connection:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        self.detail = '\033[90m'

    def unlock_register_connection(self):

        ## Name
        name = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')

        ## Contract Tab
        self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/ul/li[7]/a'))).click()

        ## Status
        status = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr[1]/td[4]/div/span')))

        if 'Bloqueio Automático' in status.text or 'Financeiro em atraso' in status.text:

            ## Actions
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/div'))).click()

            ## Trust Unlocking
            self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/ul/li[3]'))).click()

            alert = self.driver.switch_to.alert
            alert.accept()

            time.sleep(6)

            ## Refresh
            refresh_btn = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/span[1]/i[3]')))
            self.driver.execute_script('arguments[0].click();', refresh_btn)

            time.sleep(1)

            ## Status
            status = self.wait.until(located((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[4]/div/span')))

            if 'Bloqueio Automático' in status.text or 'Financeiro em atraso' in status.text:

                ## Edit Tab
                self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/button[2]'))).click()

                time.sleep(2)

                ## Status Tab
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/ul/li[5]/a'))).click()

                today = (DATETIME.define_datime_now()).split(' ')[0]

                new_date = DATETIME.define_days_timedelta(today, 2)

                ## 
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[3]/dd/input'))).clear()
                for _ in range(2): self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[3]/dd/input'))).click()
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[3]/dd/input'))).send_keys(new_date)

                ## 
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[5]/dd/input'))).clear()
                for _ in range(2): self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[5]/dd/input'))).click()
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[3]/div[5]/dl[5]/dd/input'))).send_keys(new_date)

                time.sleep(1)

                ## Save
                self.wait.until(clickable((By.XPATH, '/html/body/form[3]/div[2]/button[2]'))).click()

                time.sleep(1)
                get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

                ## Actions
                self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/div'))).click()

                ## 
                self.wait.until(clickable((By.XPATH, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/ul/li[1]'))).click()

            time.sleep(2)

            CLEAR.clear_register_connection(self)

            print(self.detail + '     ' + name + ' - Unlocked!')

        else:

            print(self.detail + '     ' + name + ' - Register not locked!')

    def search_register(self, type, id_list):
            
        try:

            ## Search
            registers = self.wait.until(located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')))
            self.driver.execute_script('arguments[0].click();', registers)

            print('\n     Unlocking...')

            for register_id in id_list:

                SEARCH.open_register_search(self, type, register_id)

                self.unlock_register_connection()

                ## Clear Name
                clear_name = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')))
                self.driver.execute_script('arguments[0].click();', clear_name)

            time.sleep(1)
            for _ in range(4): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            return ['success', ' Successfully registers connection unlocked.']
    
        except:

            return ['error', traceback.format_exc()]

