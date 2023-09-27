import time
import traceback
from selenium_core import sc
from search_register import SearchRegister as SEARCH
from traceback_formatted import traceback_formatted

class ClearConnection:
    
    def __init__(self):
        self.detail = '\033[90m'

    def clear_register_connection(self):

        ## Register
        register_name = sc.element('xpath', '/html/body/form[2]/div[3]/div[1]/dl[6]/dd/input').get_attribute('value')

        ## Login Tab
        sc.click('xpath', '/html/body/form/div[3]/ul/li[8]/a')

        ## Clear MAC
        sc.click('xpath', '/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[10]')

        sc.alert('accept')

        time.sleep(2)

        ## Disconnect Login
        sc.click('xpath', '/html/body/form/div[3]/div[8]/dl/div/div/div[2]/div[1]/button[11]')

        sc.alert('accept')

        sc.action('esc')

        return register_name

    def search_register(self, type, register_id):

        try:

            ## Search
            sc.click('xpath', '/html/body/div[1]/div[3]/div/div[1]/div[2]/ul/li[1]/a')

            SEARCH.open_register_search(self, type, register_id)

            register = self.clear_register_connection()
            
            # sc.action('esc')
            sc.refresh()
            sc.alert('accept')

            return ['success', ' Successfully register connection cleaned. ' + self.detail + '[ ' + register + ' ]']

        except:
            
            return ['error', traceback_formatted(traceback.format_exc())]

