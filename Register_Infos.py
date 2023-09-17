import time, re

from Selenium import get_wait, script_click, get_value, get_text

class Register_Infos:

    def __init__(self, driver):
        self.driver = driver
        self.wait = get_wait(self.driver)

    def get_register_infos(self, form):

        time.sleep(2)

        ## Get Name
        name = get_value(self, f'/html/body/form[{form}]/div[3]/div[1]/dl[6]/dd/input')

        ## Address
        script_click(self, f'/html/body/form[{form}]/div[3]/ul/li[2]/a')

        ## Get Condominium
        condominium = get_value(self, f'/html/body/form[{form}]/div[3]/div[2]/dl[2]/dd/input[1]')
        condominium = condominium if condominium else 0

        ## Get Block
        block = get_value(self, f'/html/body/form[{form}]/div[3]/div[2]/dl[3]/dd/input')
        block = re.sub('[a-zA-Z]', '', block)

        ## Get Apto
        apt = get_value(self, f'/html/body/form[{form}]/div[3]/div[2]/dl[4]/dd/input')
        apt = re.sub('[a-zA-Z]', '', apt)

        ## Get Complement
        complement = get_value(self, f'/html/body/form[{form}]/div[3]/div[2]/dl[9]/dd/input')
        complement = complement if complement else ''

        ## Get District
        district = get_value(self, f'/html/body/form[{form}]/div[3]/div[2]/dl[10]/dd/input')

        ## Contact
        script_click(self, f'/html/body/form[{form}]/div[3]/ul/li[3]')

        ## Get Phone
        phone = get_value(self, f'/html/body/form[{form}]/div[3]/div[3]/dl[5]/dd/input')

        ## Contract
        script_click(self, f'/html/body/form[{form}]/div[3]/ul/li[7]/a')

        ## Get Band
        band = get_text(self, f'/html/body/form[{form}]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[12]/div')

        try:

            ## Login
            script_click(self, f'/html/body/form[{form}]/div[3]/ul/li[8]/a')

            ## Get Login
            login = get_text(self, f'/html/body/form[{form}]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div')
        
        except:
            
            pass

        return [name, condominium, block, apt, complement, district, phone, login, band]

