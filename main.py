from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import sys
import unicodedata
from pprint import pprint

url = 'https://digital.stf.jus.br/publico/publicacoes'
PATH_DRIVER = 'chromedriver.exe'

data = input('Escolha uma data no padrão DD/MM/AAAA: ')
print('')
data_split = data.split('/')
dia = data_split[0]
mes = data_split[1]
ano = data_split[2]

validar = True
while  validar:
    time.sleep(0.5)
    print('OPÇÕES DE BUSCA: \n1 - Publicação \n2 - Divulgação \n3 - Sair do Programa\n')
    opcao_site = input('Escolha uma opção: ')

    if opcao_site == '1':
        time.sleep(0.5)
        print('Você escolheu a opção Publicação')
        validar = False
    elif opcao_site == '2':
        time.sleep(0.5)
        print('Você escolheu a opção Divulgação')
        validar = False
    elif opcao_site == '3':
        time.sleep(0.5)
        print('Saindo do Programa!')
        time.sleep(0.5)
        exit()
    else:
        time.sleep(0.5)
        print('\033[31m'+'Opção Inválida!'+'\033[0;0m'+'\n')
    

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')


chrome = webdriver.Chrome(options=options)
chrome.get(url)

time.sleep(5)

# Abrir arquivo
nome_arquivo = f'STF-{ano}-{mes}-{dia}.txt'
with open(nome_arquivo, 'w', encoding='utf-8') as txt:
    # Definir a data
    elem = chrome.find_element_by_xpath(
                '//*[@id="publicacoes"]/div/div/div[2]/form/div[1]/input'
                )
    elem.send_keys(ano)
    elem.send_keys(Keys.ARROW_LEFT, mes)
    elem.send_keys(Keys.ARROW_LEFT)
    elem.send_keys(Keys.ARROW_LEFT, dia)

    time.sleep(2)
    # Escolher divulgação
    chrome.find_element_by_id('select_value_label_0').click()
    time.sleep(2)
    chrome.find_element_by_id(f'select_option_{opcao_site}').click()

    time.sleep(3)
    # Pegar Conteúdo da página
    elementos = chrome.find_elements_by_class_name('white-bg')

    # Função que busca o texto escondido em shadow
    shadow_section = chrome.find_elements_by_class_name(
        'shadow'
        )

    for elem in elementos:
        html_content_elem = elem.get_attribute('outerHTML')
        soup_elem= BeautifulSoup(html_content_elem, 'html.parser')
        cabecalho = soup_elem.get_text()

        if 'Apresentando de 1 até' in cabecalho:
            continue
        
        # método para remover o /xa0
        novo_cabecalho = unicodedata.normalize("NFKD", cabecalho)
        txt.write(novo_cabecalho + "\n")
        pprint(novo_cabecalho)

        try:
            # Função que busca o texto escondido em shadow
            shadow_section = elem.find_element_by_class_name('shadow')
        except:
            continue
    
        shadow_root_dict = chrome.execute_script(
            "return arguments[0].shadowRoot", shadow_section
            )
        shadow_root_id = shadow_root_dict['shadow-6066-11e4-a52e-4f735466cecf']
        shadow_root = WebElement(chrome, shadow_root_id, w3c=True)

        content_html = shadow_root.find_elements(
            By.TAG_NAME, 'p'
            )

        for conteudo in content_html:

            html_content = conteudo.get_attribute('outerHTML')
            soup = BeautifulSoup(html_content, 'html.parser')
            texto = soup.get_text()

            # método para remover o /xa0
            novo_texto = unicodedata.normalize("NFKD", texto)
            txt.write(novo_texto + "\n")
            pprint(novo_texto)
        
time.sleep(5)
chrome.close()
