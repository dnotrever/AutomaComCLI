import time, re

from Selenium import By, Keys
from Selenium import get_wait, get_actions, clickable, located, all_located

class Register_Infos:

    def __init__(self, driver):

        self.driver = driver
        self.wait = get_wait(self.driver)
        self.actions = get_actions(self.driver)

    def get_register_infos(self, form):

        time.sleep(2)

        ## Get Name
        name = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[1]/dl[6]/dd/input'))).get_attribute('value')

        ## Address
        self.wait.until(clickable((By.XPATH, f'/html/body/form[{form}]/div[3]/ul/li[2]/a'))).click()

        ## Get Condominium
        condominium = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[2]/dl[2]/dd/input[1]'))).get_attribute('value')
        condominium = condominium if condominium else 0

        ## Get Block
        block = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[2]/dl[3]/dd/input'))).get_attribute('value')
        block = re.sub('[a-zA-Z]', '', block)

        ## Get Apto
        apt = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[2]/dl[4]/dd/input'))).get_attribute('value')
        apt = re.sub('[a-zA-Z]', '', apt)

        ## Get Complement
        complement = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[2]/dl[9]/dd/input'))).get_attribute('value')
        complement = complement if complement else ''

        ## Get District
        district = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[2]/dl[10]/dd/input'))).get_attribute('value')

        ## Contact
        self.wait.until(clickable((By.XPATH, f'/html/body/form[{form}]/div[3]/ul/li[3]'))).click()

        ## Get Phone
        phone = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[3]/dl[5]/dd/input'))).get_attribute('value')

        ## Contract
        self.wait.until(clickable((By.XPATH, f'/html/body/form[{form}]/div[3]/ul/li[7]/a'))).click()

        ## Get Band
        band = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[7]/dl/div/div/div[5]/table/tbody/tr/td[12]/div'))).text

        ## Login
        self.wait.until(clickable((By.XPATH, f'/html/body/form[{form}]/div[3]/ul/li[8]'))).click()

        ## Get Login
        login = self.wait.until(located((By.XPATH, f'/html/body/form[{form}]/div[3]/div[8]/dl/div/div/div[5]/table/tbody/tr/td[11]/div'))).text

        return [name, condominium, block, apt, complement, district, phone, login, band]

