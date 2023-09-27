import os
from dotenv import load_dotenv
from selenium_core import sc

class SystemsAccess:

    def __init__(self):

        load_dotenv()

        self.sys_1_url = os.getenv('SYS_1_URL')
        self.sys_1_email = os.getenv('SYS_1_EMAIL')
        self.sys_1_pass = os.getenv('SYS_1_PASS')

        self.sys_2_url = os.getenv('SYS_2_URL')
        self.sys_2_email = os.getenv('SYS_2_EMAIL')
        self.sys_2_pass = os.getenv('SYS_2_PASS')
    
    def system_1_access(self):

        sc.get(self.sys_1_url)

        sc.element('xpath', '/html/body/div[3]/div/div[4]/form/div[2]/input').send_keys(self.sys_1_email)
        sc.element('xpath', '/html/body/div[3]/div/div[4]/form/div[3]/input').send_keys(self.sys_1_pass)

        sc.click('xpath', '/html/body/div[3]/div/div[4]/form/div[4]/div[1]/i')

        sc.click('xpath', '/html/body/div[3]/div/div[4]/form/div[5]/button[2]')

        try:
            if sc.element('selector', 'div[class="alerts"]'):
                sc.click('xpath', '/html/body/div[3]/div/div[4]/form/div[5]/button[2]')
        except:
            pass

    def system_2_access(self):

        sc.get(self.sys_2_url)

        sc.element('xpath', '/html/body/div/div[2]/div[2]/form/div[1]/input').send_keys(self.sys_2_email)
        sc.element('xpath', '/html/body/div/div[2]/div[2]/form/div[2]/input').send_keys(self.sys_2_pass)

        sc.click('xpath', '/html/body/div/div[2]/div[2]/form/div[4]/div[1]/button')

        try:
            sc.click('xpath', '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')
        except:
            pass

