import time

from Selenium import interaction, action

class Search_Register:

    def __init__(self, driver):
        self.driver = driver

    def open_register_search(self, type, register_label):

        driver = self.driver

        if type == 'id':

            ## ID Button
            interaction(driver, 'click', '/html/body/div[2]/div/div[3]/nav/ul/li[2]')

        ## Insert Input ID
        interaction(driver, 'send_keys', '/html/body/div[2]/div/div[3]/div/input', register_label)

        time.sleep(2)

        for _ in range(2):
            action(driver, 'enter')

        time.sleep(1)

        if type == 'name':

            registers_list = interaction(driver, 'selector_all', 'tr[data-campoautoincrement="id"]')

            for customer in registers_list:

                ## Customer Name
                # name_parent = get_wait(customer).until(located((By.CSS_SELECTOR, 'td[abbr="cliente.razao"]')))
                # name_child = get_wait(name_parent).until(located((By.TAG_NAME, 'div')))
                name = interaction(customer, 'selector', 'td[abbr="cliente.razao"]')

                ## Is Customer and is Selected? Pass!
                if register_label.lower() == name.text.lower() and customer.get_attribute('class') == 'trSelected':
                    break
                
                ## Is Customer and Not Selected? Selected and Pass!
                if register_label.lower() == name.text.lower():
                    interaction(driver, 'click', name)
                    break
        
        ## Register Edit
        interaction(driver, 'click', '/html/body/div[2]/div/div[2]/div[1]/button[2]')

        time.sleep(1)

