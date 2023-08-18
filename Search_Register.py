import time, re

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

class Search_Register:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def open_register_search(self, type, register_label):

        if type == 'id':

            ## ID Button
            id_btn = self.wait.until(located((By.CSS_SELECTOR, r'#\31 _grid > div > div.sDiv > nav > ul > li:nth-child(2)')))
            self.driver.execute_script('arguments[0].click();', id_btn)

            ## Insert Input ID
            self.wait.until(located((By.CSS_SELECTOR, 'input[name="q"]'))).send_keys(register_label)
        
        if type == 'name':

            ## Insert Input Name
            self.wait.until(located((By.CSS_SELECTOR, 'input[name="q"]'))).send_keys(register_label)

        time.sleep(1)

        for _ in range(3): get_actions(self.driver).send_keys(Keys.ENTER).perform()

        time.sleep(3)

        if type == 'name':

            registers_list = self.wait.until(all_located((By.CSS_SELECTOR, 'tr[data-campoautoincrement="id"]')))

            for customer in registers_list:

                ## Customer Name
                name_parent = get_wait(customer).until(located((By.CSS_SELECTOR, 'td[abbr="cliente.razao"]')))
                name_child = get_wait(name_parent).until(located((By.TAG_NAME, 'div')))

                ## Is Customer and is Selected? Pass!
                if register_label.lower() == name_child.text.lower() and customer.get_attribute('class') == 'trSelected':
                    break
                
                ## Is Customer and Not Selected? Selected and Pass!
                if register_label.lower() == name_child.text.lower():
                    self.driver.execute_script('arguments[0].click();', name_child)
                    break
        
        ## Register Infos
        edit_btn = self.wait.until(located((By.CSS_SELECTOR, 'button[name="editar"]')))
        self.driver.execute_script('arguments[0].click();', edit_btn)

        time.sleep(1)

