import time, traceback

from SeleniumCore import Keys
from SeleniumCore import get_wait, get_actions, script_click, get_value, get_text, send_keys, clear_input, perform_esc

from Search_Register import Search_Register as SEARCH
from Set_DateTime import Set_DateTime as DATETIME
from Clear_Connection import Clear_Connection as CLEAR

from traceback_formatted import traceback_formatted

class Unlock_Connection:

    def __init__(self, driver):
        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)
        self.detail = '\033[90m'

    def unlock_register_connection(self):

        ## Name
        name = get_value(self, '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input')

        ## Contract Tab
        script_click(self, '/html/body/form[2]/div[3]/ul/li[7]/a')

        ## Status
        status = get_text(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr[1]/td[4]/div/span')

        if 'Bloqueio Automático' in status or 'Financeiro em atraso' in status:

            ## Actions
            script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/div')

            ## Trust Unlocking
            script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/ul/li[3]')

            alert = self.driver.switch_to.alert
            alert.accept()

            time.sleep(6)

            ## Refresh
            script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/span[1]/i[3]')

            time.sleep(1)

            ## Status
            status = get_text(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr[1]/td[4]/div/span')

            if 'Bloqueio Automático' in status or 'Financeiro em atraso' in status:

                ## Edit Tab
                script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/button[2]')

                time.sleep(2)

                ## Status Tab
                script_click(self, '/html/body/form[3]/div[3]/ul/li[5]/a')

                today = (DATETIME.define_datime_now()).split(' ')[0]

                new_date = DATETIME.define_days_timedelta(today, 2)

                ## Date 1
                date1 = '/html/body/form[3]/div[3]/div[5]/dl[3]/dd/input'
                clear_input(self, date1)
                script_click(self, date1)
                send_keys(self, date1, new_date)

                ## Date 2
                date2 = '/html/body/form[3]/div[3]/div[5]/dl[5]/dd/input'
                clear_input(self, date2)
                script_click(self, date2)
                send_keys(self, date2, new_date)

                time.sleep(1)

                ## Save
                script_click(self, '/html/body/form[3]/div[2]/button[2]')

                perform_esc(self.actions)

                ## Actions
                script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/div')

                ## 
                script_click(self, '/html/body/form[2]/div[3]/div[7]/dl/div/div/div[2]/div[1]/nav[1]/ul/li[1]')

            time.sleep(2)

            CLEAR.clear_register_connection(self)

            print(self.detail + '     ' + name + ' - Unlocked!')

        else:

            print(self.detail + '     ' + name + ' - Register not locked!')

    def search_register(self, type, id_list):
            
        try:

            ## Search
            script_click(self, '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')

            print('\n     Unlocking...')

            for register_id in id_list:

                SEARCH.open_register_search(self, type, register_id)

                self.unlock_register_connection()

                ## Clear Name
                # clear_name = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > div > div:nth-child(2) > span > i')))
                # self.driver.execute_script('arguments[0].click();', clear_name)
                clear_input(self, '/html/body/div[2]/div/div[3]/div/input')

            time.sleep(1)
            for _ in range(4): get_actions(self.driver).send_keys(Keys.ESCAPE).perform()

            return ['success', ' Successfully registers connection unlocked.']
    
        except:

            return ['error', traceback_formatted(traceback.format_exc())]

