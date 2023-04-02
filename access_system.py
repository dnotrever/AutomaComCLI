import Selenium as SEL
import CONF
from Selenium import By, Keys
from Selenium import clickable, located

driver = SEL.get_driver()
wait = SEL.get_wait(driver)
actions = SEL.get_actions(driver)

def open_system(system, op_code):

    if system == 1:

        url = CONF.systems(1)
        email = CONF.credentials(op_code)[0]
        password = CONF.credentials(op_code)[1]

        driver.get(url)

        wait.until(located((By.NAME, 'email'))).send_keys(email)
        wait.until(located((By.NAME, 'senha'))).send_keys(password)

        wait.until(located((By.ID, 'entrar'))).click()
            
        if wait.until(located((By.ID, 'resp'))):
            try: wait.until(clickable((By.ID, 'entrar'))).click()
            except: pass

    if system == 2:

        url = CONF.systems(2)
        email = CONF.sys_2_cred[0]
        password = CONF.sys_2_cred[1]

        driver.get(url)

        wait.until(located((By.NAME, 'username'))).send_keys(email)
        wait.until(located((By.NAME, 'password'))).send_keys(password)

        wait.until(located((By.ID, 'btn_login'))).click()

        try: wait.until(clickable((By.CLASS_NAME, 'btn-blue'))).click()
        except: pass
