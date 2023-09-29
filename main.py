import os
import time
from selenium_core import sc
from systems_access import SystemsAccess
from Set_DateTime import Set_DateTime as DATETIME

sc.set_driver()

SystemsAccess().system_1_access()

os.system('cls')

# os.system('mode con: cols=125 lines=25')

historic = []

messageColors = {
    'others': '\033[1;34m', ## purple
    'success': '\033[32m', ## green
    'error': '\033[31m', ## red
    'info': '\033[36m', ## blue
    'detail': '\033[90m', ## gray
    'reset': '\033[0m', ## reset color
}

others, success, error, info, detail, reset = messageColors.values()

parag = f'\n {others}$ ~{reset} '

def message(msg):

    if msg[0] == 'success':
        print(parag + detail + DATETIME.now_format() + success + msg[1] + reset)

    if msg[0] == 'error':
        print('\n' + error + 'An error has occurred:')
        print('\n' + detail + msg[1] + reset)

def command_line():

    option = input(parag).split(' ')

    sc.refresh()

    try: sc.alert('accept')
    except: pass

    time.sleep(3)

    ## Services
    if option[0] == 'services':

        from services_list import services
        msg = services.services_infos()

    ## Emergency
    if option[0] == 'emerg':

        register_id = option[1]
        service = option[2]

        from Emergency import Emergency
        msg = Emergency(driver).register_verify('id', register_id, service)

    ## Closing Services
    if option[0] == 'close':

        if option[1] == 'verify':

            date = option[2] if len(option) > 2 else 'today'

            from closing_services import ClosingServices
            msg = ClosingServices().closing_verify(date)

        if option[1] == 'execute':

            from closing_services import ClosingServices
            msg = ClosingServices().closing_execute()
    
    ## Scheduling Services
    if option[0] == 'schedule':

        if option[1] == 'verify':

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            from systems_access import Systems
            Systems(driver).system_2_access()

            from Scheduling_Services import Scheduling_Services
            msg = Scheduling_Services(driver).scheduling_verify()

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        if option[1] == 'execute':
            from Scheduling_Services import Scheduling_Services
            msg = Scheduling_Services(driver).scheduling_execute()

    ## Multiple Registers
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
        from clear_connection import ClearConnection
        msg = ClearConnection().search_register('id', register_id)

    ## Contract Activation
    if option[0] == 'contract':

        from Contract_Activation import Contract_Activation
        msg = Contract_Activation(driver).contract_activation()
        
    ## Attendances Transfer
    if option[0] == 'transfer':

        sc.tab(1)

        from systems_access import SystemsAccess
        SystemsAccess().system_2_access()

        from attendances import Attendances
        code = option[1] if len(option) > 1 else '0'
        msg = Attendances().transfer(code)

        sc.close()
        sc.tab(0)

    ## Attendances Message
    if option[0] == 'message':

        tags = input(f'\n {info}>>{reset}  ').split(' - ')

        main_tag = tags[0] 
        counter_tag = tags[1] if len(tags) > 1 else 'not-used'
        finish = tags[2] if len(tags) > 2 else False

        text = input(f'\n {info}>>{reset}  ')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])

        from systems_access import Systems
        Systems(driver).system_2_access()

        from attendances import Attendances
        code = option[1] if len(option) > 1 else '0'
        msg = Attendances(driver).message(main_tag, counter_tag, finish, text)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    ## Terminal Historic
    if option[0] == 'hist':
        print(detail)
        for hist in historic:
            print('    ' + DATETIME.now_format() + ' ' + detail + hist + reset)

    ## Terminal Clean
    if option[0] == 'clear':
        os.system('cls')

    try:
        historic.append(msg[1])
        message(msg)
    except:
        pass

    command_line()

command_line()
