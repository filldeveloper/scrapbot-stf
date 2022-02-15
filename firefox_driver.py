from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import sys
import unicodedata
from pprint import pprint


url = 'https://digital.stf.jus.br/publico/publicacoes'

data = input('Escolha uma data no padrão DD/MM/AAAA: ')
print('')
data_split = data.split('/')
dia = data_split[0]
mes = data_split[1]
ano = data_split[2]

print(f'Dia: {dia}')
print(f'Mes: {mes}')
print(f'ano: {ano}')
exit()

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
    
driver = webdriver.Firefox()

driver.get(url)

nome_arquivo = f'STF-{ano}-{mes}-{dia}.txt'
sleep(4)
with open(nome_arquivo, 'w', encoding='utf-8') as txt:
    # Definir a data
    elem = driver.find_element_by_class_name(
                    'data-pesquisa')
    sleep(1)
    elem.click()
    elem.send_keys(ano)
    elem.send_keys(Keys.ARROW_LEFT, mes)
    elem.send_keys(Keys.ARROW_LEFT)
    elem.send_keys(Keys.ARROW_LEFT, dia)

    sleep(2)
    # Escolher divulgação
    driver.find_element_by_id('select_value_label_0').click()
    sleep(2)
    driver.find_element_by_id(f'select_option_{opcao_site}').click()

    sleep(3)

