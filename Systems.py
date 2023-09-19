import os
from dotenv import load_dotenv

from Selenium import interaction

class Systems:

    def __init__(self, driver):

        self.driver = driver

        load_dotenv()

        self.sys_1_url = os.getenv('SYS_1_URL')
        self.sys_1_email = os.getenv('SYS_1_EMAIL')
        self.sys_1_pass = os.getenv('SYS_1_PASS')

        self.sys_2_url = os.getenv('SYS_2_URL')
        self.sys_2_email = os.getenv('SYS_2_EMAIL')
        self.sys_2_pass = os.getenv('SYS_2_PASS')
    
    def system_1_access(self):

        driver = self.driver

        driver.get(self.sys_1_url)

        interaction(driver, 'send_keys', '/html/body/div[3]/div/div[4]/form/div[2]/input', self.sys_1_email)
        interaction(driver, 'send_keys', '/html/body/div[3]/div/div[4]/form/div[3]/input', self.sys_1_pass)

        interaction(driver, 'click', '/html/body/div[3]/div/div[4]/form/div[4]/div[1]/i')

        interaction(driver, 'click', '/html/body/div[3]/div/div[4]/form/div[5]/button[2]')

        if interaction(driver, 'selector', 'div[class="alerts"]'):

            try:
                interaction(driver, 'click', '/html/body/div[3]/div/div[4]/form/div[5]/button[2]')

            except:
                pass

    def system_2_access(self):

        driver = self.driver

        driver.get(self.sys_2_url)

        interaction(driver, 'send_keys', '/html/body/div/div[2]/div[2]/form/div[1]/input', self.sys_2_email)
        interaction(driver, 'send_keys', '/html/body/div/div[2]/div[2]/form/div[2]/input', self.sys_2_pass)

        interaction(driver, 'click', '/html/body/div/div[2]/div[2]/form/div[4]/div[1]/button')

        try:
            interaction(driver, 'click', '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button[2]')

        except:
            pass

