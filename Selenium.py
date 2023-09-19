import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--lang=pt-br')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def wait_located(driver, element, mode='xpath', timeout=30):
    if mode == 'xpath':
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element)))
    if mode == 'selector':
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))

def wait_all_located(driver, element, mode='xpath', timeout=30):
    if mode == 'xpath':
        return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, element)))
    if mode == 'selector':
        return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, element)))

def interaction(driver, type, element, keys=''):

    #--- XPath (default) ---#

    if type == 'get':
        return wait_located(driver, element)
    
    if type == 'get_all':
        return wait_all_located(driver, element)
    
    if type == 'click':
        return driver.execute_script('arguments[0].click();', wait_located(driver, element))
    
    if type == 'click --e':
        return driver.execute_script('arguments[0].click();', element)
    
    if type == 'send_keys':
        return wait_located(driver, element).send_keys(keys)
    
    if type == 'clear':
        return wait_located(driver, element).clear()
    
    if type == 'text':
        return wait_located(driver, element).text
    
    if type == 'value':
        return wait_located(driver, element).get_attribute('value')
    
    #--- Others (default) ---#

    if type == 'selector':
        return wait_located(driver, element, 'selector')
    
    if type == 'selector_all':
        return wait_all_located(driver, element, 'selector')

def action(driver, key, element=''):

    time.sleep(1)

    if key == 'esc':
        return ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    if key == 'enter':
        return ActionChains(driver).send_keys(Keys.ENTER).perform()
    
    if key == 'up':
        return ActionChains(driver).send_keys(Keys.UP).perform()
    
    if key == 'tab':
        return ActionChains(driver).send_keys(Keys.TAB).perform()
    
    if key == 'double':
        return ActionChains(driver).double_click(element).perform()
    

##  WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '')))