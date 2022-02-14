from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd 
import time 
from pprint import pprint

url = 'https://digital.stf.jus.br/publico/publicacoes'
PATH_DRIVER = '/home/serpro/development/google-sheet/Google-sheet/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

chrome = webdriver.Chrome(PATH_DRIVER, 
                            options=options
)
chrome.get(url)

data = '05/02/2022'
time.sleep(5)

# Definir a data
elem = chrome.find_element_by_xpath(
            '//*[@id="publicacoes"]/div/div/div[2]/form/div[1]/input'
            )
elem.send_keys('2022')
elem.send_keys(Keys.ARROW_LEFT, '02')
elem.send_keys(Keys.ARROW_LEFT)
elem.send_keys(Keys.ARROW_LEFT, '11')

time.sleep(2)
# Escolher divulgação
chrome.find_element_by_id('select_value_label_0').click()
chrome.find_element_by_id('select_option_2').click()

time.sleep(3)
# Pegar Conteúdo da página
# elem = chrome.find_element_by_xpath('//*[@id="conteudo"]/div[2]/md-content')
# html_content = elem.get_attribute('outerHTML')
# soup = BeautifulSoup(html_content, 'html.parser')
# pprint(soup)




# def expand_shadow_element(element):
#     shadow_root = chrome.execute_script('return arguments[0].shadowRoot', element)
#     return shadow_root

shadow_section = chrome.find_elements_by_class_name(
    'shadow'
    )
for shadow in shadow_section:
# shadow_root = chrome.execute_script("return arguments[0].shadowRoot", shadow_section)
    shadow_root_dict = chrome.execute_script(
        "return arguments[0].shadowRoot", shadow
        )

    shadow_root_id = shadow_root_dict['shadow-6066-11e4-a52e-4f735466cecf']
    shadow_root = WebElement(chrome, shadow_root_id, w3c=True)


    content_html = shadow_root.find_elements(
        By.TAG_NAME, 'p'
        )

    for conteudo in content_html:

        html_content = conteudo.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        texto = soup.get_text('\n')
        pprint(texto)
# for i in elem:
#     html_content = i.get_attribute('outerHTML')
#     soup = BeautifulSoup(html_content, 'html.parser')
#     texto = soup.get_text('\n')
#     pprint(texto)
#     exit()
time.sleep(5)
chrome.close()
