import traceback, os

from Selenium import get_driver
from Systems import Systems

driver = get_driver()

Systems(driver).system_1_access()

os.system('cls')

# os.system('mode con: cols=125 lines=25')

messageColors = {
    'others': '\033[1;34m', ## purple
    'success': '\033[0;32m', ## green
    'error': '\033[1;31m', ## red
    'info': '\033[36m', ## blue
    'detail': '\033[1;90m', ## gray
    'reset': '\033[0;0m',
}

others, success, error, info, detail, reset = messageColors.values()

parag = f'\n {others}$~{reset}  '

def message(msg):

    color = success if msg[0] == 'success' else error
    print(parag + color + msg[1] + reset)

def commandline():

    option = input(parag).split(' ')

    try:

        ## Services
        if option[0] == 'services':

            from Services import Services
            msg = Services(driver).services_infos()

        ## Emergency
        if option[0] == 'emerg':

            register_id = option[1]
            service = option[2]

            from Emergency import Emergency
            msg = Emergency(driver).register_verify('id', register_id, service)

        ## Closing Services
        if option[0] == 'close':

            if option[1] == 'verify':

                from Closing_Services import Closing_Services
                msg = Closing_Services(driver).closing_verify()

            if option[1] == 'execute':

                from Closing_Services import Closing_Services
                msg = Closing_Services(driver).closing_execute()
        
        ## Scheduling Services
        if option[0] == 'schedule':

            if option[1] == 'verify':

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])

                from Systems import Systems
                Systems(driver).system_2_access()

                from Scheduling_Services import Scheduling_Services
                msg = Scheduling_Services(driver).scheduling_verify()

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            if option[1] == 'execute':
                from Scheduling_Services import Scheduling_Services
                msg = Scheduling_Services(driver).scheduling_execute()

        ## Multiple
        if option[0] == 'multiple':

            from Multiple_Registers import Multiple_Registers
            msg = Multiple_Registers(driver).multiple_verify()

        ## Removals
        if option[0] == 'removals':

            from Removals import Removals
            msg = Removals(driver).removals_verify()

        ## Unlock Connection
        if option[0] == 'unlock':

            id_list = option[1].split('-')
            from Unlock_Connection import Unlock_Connection
            msg = Unlock_Connection(driver).search_register('id', id_list)

        ## Clear Connection
        if option[0] == 'disc':

            register_id = option[1]
            from Clear_Connection import Clear_Connection
            msg = Clear_Connection(driver).search_register('id', register_id)

        ## Contract Activation
        if option[0] == 'contract':

            from Contract_Activation import Contract_Activation
            msg = Contract_Activation(driver).contract_activation()
            
        ## Attendances
        if option[0] == 'transfer':

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            from Systems import Systems
            Systems(driver).system_2_access()

            from Attendances import Attendances
            code = option[1] if len(option) > 1 else '0'
            msg = Attendances(driver).transfer(code)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        ## Terminal Clean
        if option[0] == 'clear':
            os.system('cls')

        try: message(msg)
        except: pass

    except Exception as err:
        print(f'\n{error}An error has occurred:\n\n{detail}{traceback.format_exc()}{reset}')
    
    finally:
        commandline()

commandline()


# XPATH Customer Infos
# OS (Register)  -->   /html/body/form[3]/ ...
# Customers      -->   /html/body/form[2]/ ...