import time
import re

from selenium_core import sc

class RegisterInfos:

    def get_register_infos(form):

        time.sleep(2)

        ## Get Name
        name = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[1]/dl[6]/dd/input').get_attribute('value')

        print(f'     {name}')

        ## Address
        sc.click('xpath', f'/html/body/form[{form}]/div[3]/ul/li[2]/a')

        ## Get Condominium
        condominium = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[2]/dl[2]/dd/input[1]').get_attribute('value')
        condominium = condominium if condominium else 0

        ## Get Block
        block = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[2]/dl[3]/dd/input').get_attribute('value')
        block = re.sub('[a-zA-Z]', '', block)

        ## Get Apto
        apt = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[2]/dl[4]/dd/input').get_attribute('value')
        apt = re.sub('[a-zA-Z]', '', apt)

        ## Get Complement
        complement = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[2]/dl[9]/dd/input').get_attribute('value')
        complement = complement if complement else ''

        ## Get District
        district = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[2]/dl[10]/dd/input').get_attribute('value')

        ## Contact
        sc.click('xpath', f'/html/body/form[{form}]/div[3]/ul/li[3]')

        ## Get Phone
        phone = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[3]/dl[5]/dd/input').get_attribute('value')

        ## Contract
        sc.click('xpath', f'/html/body/form[{form}]/div[3]/ul/li[7]/a')

        ## Get Band
        band = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[12]/div').text

        try:

            ## Login
            sc.click('xpath', f'/html/body/form[{form}]/div[3]/ul/li[8]/a')

            ## Get Login
            login = sc.element('xpath', f'/html/body/form[{form}]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div').text
        
        except:
            
            login = ''

        return [name, condominium, block, apt, complement, district, phone, login, band]

