from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from functions import *
from time import sleep
import sys
import os
import math
import unicodedata
from pprint import pprint

url = 'https://digital.stf.jus.br/publico/publicacoes'
PATH_DRIVER = 'chromedriver.exe'
# Apresentar o número de registros encontrados e baixados

data = input('Escolha uma data no padrão DD/MM/AAAA: ')
print('')
data_split = data.split('/')
dia = data_split[0]
mes = data_split[1]
ano = data_split[2]

validar = True
while  validar:
    sleep(0.5)
    print('OPÇÕES DE BUSCA: \n1 - Publicação \n2 - Divulgação \n3 - Sair do Programa\n')
    opcao_site = input('Escolha uma opção: ')

    if opcao_site == '1':
        sleep(0.5)
        print('Você escolheu a opção Publicação')
        validar = False
    elif opcao_site == '2':
        sleep(0.5)
        print('Você escolheu a opção Divulgação')
        validar = False
    elif opcao_site == '3':
        sleep(0.5)
        print('Saindo do Programa!')
        sleep(0.5)
        exit()
    else:
        sleep(0.5)
        print('\033[31m'+'Opção Inválida!'+'\033[0;0m'+'\n')
    

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')


chrome = webdriver.Chrome(options=options)
chrome.get(url)

sleep(5)

# Abrir arquivo
nome_arquivo = f'C:/sei-dj/stf/STF-{ano}-{mes}-{dia}.txt'
with open(nome_arquivo, 'w', encoding='utf-8') as txt:
    # Definir a data
    elem = chrome.find_element_by_xpath(
                '//*[@id="publicacoes"]/div/div/div[2]/form/div[1]/input'
                )
    elem.send_keys(ano)
    elem.send_keys(Keys.ARROW_LEFT, mes)
    elem.send_keys(Keys.ARROW_LEFT)
    elem.send_keys(Keys.ARROW_LEFT, dia)

    sleep(2)
    # Escolher divulgação
    chrome.find_element_by_id('select_value_label_0').click()
    sleep(2)
    chrome.find_element_by_id(f'select_option_{opcao_site}').click()
    sleep(3)

    # Pegar quantos registros foram encontrados
    registros = chrome.find_element_by_class_name('dataTables_info')
    html_registros = registros.get_attribute('outerHTML')
    soup_registros = BeautifulSoup(html_registros, 'html.parser')
    num_registros = soup_registros.get_text().split(' ')[1]

    # Definir o numero de vezes que ira percorrer as paginas
    range_loop = int(num_registros) / 10
    range_loop = math.ceil(range_loop)

    # Print on the screen the number of pages and registers
    print(f'\nForam encontrados {num_registros} registros em {range_loop} páginas!')
    
    
    # Loop a ser feito nas paginas
    count = 1
    for number in range(range_loop):

        # Pegar Conteúdo da página
        elementos = chrome.find_elements_by_class_name('publicacoes')
    

        # Função que busca o texto escondido em shadow
        # shadow_section = chrome.find_elements_by_class_name(
        #     'shadow'
        #     )

        for elem in elementos:

            # if 'Apresentando de' in cabecalho and 'registros' in cabecalho:
            #     continue
            
            # método para remover o /xa0
            # novo_cabecalho = unicodedata.normalize("NFKD", cabecalho)

            
            # Pegar número do processo
            processo = elem.find_element(By.CLASS_NAME, 'processo')
            text_processo = outer_html(processo)

            if not text_processo:
                continue
            # Após os testes substituir o print por txt.write()
            txt.write(f'<P>{text_processo}' + "\n")
            
            # Pegar os dados do relator
            relator = elem.find_element(By.CLASS_NAME, 'relator')
            text_relator = outer_html(relator)
            txt.write(text_relator + "\n")

            # Pegar a data do despacho
            despacho = elem.find_element(
                By.XPATH, '//*[@id="conteudo"]/div[2]/md-content/div[2]/div[1]/div[2]'
                )
            text_despacho = outer_html(despacho)
            txt.write(text_despacho + "\n")

            # Pegar os dados dos envolvidos no processo
            envolvidos = elem.find_elements(By.CLASS_NAME, 'envolvido')
            for envolvido in envolvidos:
                text_envolvido = outer_html(envolvido)
                txt.write(text_envolvido + "\n")
            
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

                if len(texto) < 3:
                    continue
                # método para remover o /xa0
                novo_texto = unicodedata.normalize("NFKD", texto)
                txt.write(novo_texto + "\n")
                # print(novo_texto)
            
        # Display on the screen the number of pages recorded
        print(f'Página {count} gravada!')

        # Condition to don't click the next button in case of last page
        if count == range_loop:
            print('\nTodos os registros gravados')
            continue
        
        count += 1
        # Function to press the next button
        chrome.find_element_by_xpath(
            '//*[@id="conteudo"]/div[2]/md-content/div[1]/dir-pagination-controls/div/div[2]/div[2]/div/a[2]'
            ).click()
        sleep(1)
        

chrome.close()
print('\nPressione Ctrl + C para finalizar o programa!')

# Developed by Felipe Barreto da Silva
