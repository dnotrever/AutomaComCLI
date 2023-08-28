import os
from dotenv import load_dotenv

from Selenium import By
from Selenium import get_wait, get_actions, clickable, located

class Systems:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

        load_dotenv()

        self.sys_1_url = os.getenv('SYS_1_URL')
        self.sys_1_email = os.getenv('SYS_1_EMAIL')
        self.sys_1_pass = os.getenv('SYS_1_PASS')

        self.sys_2_url = os.getenv('SYS_2_URL')
        self.sys_2_email = os.getenv('SYS_2_EMAIL')
        self.sys_2_pass = os.getenv('SYS_2_PASS')
    
    def system_1_access(self):

        self.driver.get(self.sys_1_url)

        self.wait.until(located((By.NAME, 'email'))).send_keys(self.sys_1_email)
        self.wait.until(located((By.NAME, 'senha'))).send_keys(self.sys_1_pass)

        self.wait.until(clickable((By.ID, 'guarda_mail'))).click()

        self.wait.until(located((By.ID, 'entrar'))).click()
            
        if self.wait.until(located((By.ID, 'resp'))):
            try: self.wait.until(clickable((By.ID, 'entrar'))).click()
            except: pass

    def system_2_access(self):

        self.driver.get(self.sys_2_url)

        self.wait.until(located((By.NAME, 'username'))).send_keys(self.sys_2_email)
        self.wait.until(located((By.NAME, 'password'))).send_keys(self.sys_2_pass)

        self.wait.until(clickable((By.ID, 'btn_login'))).click()

        try: self.wait.until(clickable((By.CLASS_NAME, 'btn-blue'))).click()
        except: pass


