import time
from selenium_core import sc

class SearchRegister:

    def open_register_search(self, type, register_label):

        if type == 'id':

            ## ID Button
            sc.click('xpath', '/html/body/div[2]/div/div[3]/nav/ul/li[2]')

        ## Insert Input ID
        sc.element('xpath', '/html/body/div[2]/div/div[3]/div/input').send_keys(register_label)

        time.sleep(2)

        for _ in range(2):
            sc.action('enter')

        time.sleep(1)

        if type == 'name':

            registers_list = sc.element('xpath', 'tr[data-campoautoincrement="id"]', 'all')

            for customer in registers_list:

                ## Customer Name
                name = sc.element('selector', 'td[abbr="cliente.razao"]', 'one', customer)

                ## Is Customer and is Selected? Pass!
                if register_label.lower() == name.text.lower() and customer.get_attribute('class') == 'trSelected':
                    break
                
                ## Is Customer and Not Selected? Selected and Pass!
                if register_label.lower() == name.text.lower():
                    sc.click('none', name)
                    break
        
        ## Register Edit
        sc.click('xpath', '/html/body/div[2]/div/div[2]/div[1]/button[2]')

        time.sleep(1)

