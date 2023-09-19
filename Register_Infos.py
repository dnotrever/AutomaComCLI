import time, re

from Selenium import interaction

class Register_Infos:

    def get_register_infos(driver, form):

        time.sleep(2)

        ## Get Name
        name = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[1]/dl[6]/dd/input')

        ## Address
        interaction(driver, 'click', f'/html/body/form[{form}]/div[3]/ul/li[2]/a')

        ## Get Condominium
        condominium = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[2]/dl[2]/dd/input[1]')
        condominium = condominium if condominium else 0

        ## Get Block
        block = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[2]/dl[3]/dd/input')
        block = re.sub('[a-zA-Z]', '', block)

        ## Get Apto
        apt = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[2]/dl[4]/dd/input')
        apt = re.sub('[a-zA-Z]', '', apt)

        ## Get Complement
        complement = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[2]/dl[9]/dd/input')
        complement = complement if complement else ''

        ## Get District
        district = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[2]/dl[10]/dd/input')

        ## Contact
        interaction(driver, 'click', f'/html/body/form[{form}]/div[3]/ul/li[3]')

        ## Get Phone
        phone = interaction(driver, 'value', f'/html/body/form[{form}]/div[3]/div[3]/dl[5]/dd/input')

        ## Contract
        interaction(driver, 'click', f'/html/body/form[{form}]/div[3]/ul/li[7]/a')

        ## Get Band
        band = interaction(driver, 'text', f'/html/body/form[{form}]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[12]/div')

        try:

            ## Login
            interaction(driver, 'click', f'/html/body/form[{form}]/div[3]/ul/li[8]/a')

            ## Get Login
            login = interaction(driver, 'text', f'/html/body/form[{form}]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div')
        
        except:
            
            pass

        return [name, condominium, block, apt, complement, district, phone, login, band]

