from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from functions import *
from time import sleep
from datetime import datetime
import sys
import os
import math
import unicodedata
import pandas as pd
from pprint import pprint

url = 'https://digital.stf.jus.br/publico/publicacoes'
PATH_DRIVER = 'chromedriver.exe'
# Apresentar o número de registros encontrados e baixados

date_hour_start = datetime.today().strftime('%d/%m/%Y %H:%M')

print('OPÇÕES DE PROGRAMAS: \n1 - Novo Arquivo \n2 - Arquivo existente\n')
menu_opcoes = input('Escolha uma opção: ')
if menu_opcoes == '2':
    continuar_parametro()

data = input('Escolha uma data no padrão DD/MM/AAAA: ')
print('')
data_split = data.split('/')
dia = data_split[0]
mes = data_split[1]
ano = data_split[2]
time_pd = f'{ano}-{mes}-{dia}'
timestamp = pd.Timestamp(time_pd)
name_day = timestamp.day_name()
dia_da_semana = day_of_week(name_day)
nome_mes = name_month(mes)

validar = True
while  validar:
    sleep(0.5)
    print('OPÇÕES DE BUSCA: \n1 - Publicação \n2 - Divulgação \n3 - Sair do Programa\n')
    opcao_site = input('Escolha uma opção: ')

    if opcao_site == '1':
        sleep(0.5)
        print('Você escolheu a opção Publicação')
        opcao_texto = 'Publicação'
        validar = False
    elif opcao_site == '2':
        sleep(0.5)
        print('Você escolheu a opção Divulgação')
        opcao_texto = 'Divulgação'
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
caminho_arquivo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}.txt'
nome_arquivo = f'STFSITE-{ano}.{mes}.{dia}.txt'
caminho_resumo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-Resumo.txt'
caminho_num_processos = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-NumProcessos.txt'

# Gerando arquivo que contém somente os números dos processos
num_processos_file = open(caminho_num_processos, 'w')
num_processos_file.write(caminho_num_processos + '\n')
num_processos_file.write('=' * 54 + '\n')

# Gerando o arquivo de resumo
with open(caminho_resumo, 'w') as resumo:
    first_row = f'STFSITE: {opcao_texto}: {dia}/{mes}/{ano} ARQUIVO: {nome_arquivo}'
    resumo.write(first_row + '\n')

try:
    # Gerando o arquivo que contém os dados dos processos
    with open(caminho_arquivo, 'w') as txt:
        cabecalho = f'{opcao_texto}: {dia_da_semana}, {dia} de {nome_mes} de {ano} - STF - SITE'
        site = 'SITE DO STF'
        txt.write(cabecalho + '\n')
        txt.write(site + '\n')
        # Definir a data
        elem = chrome.find_element_by_xpath(
                    '//*[@id="publicacoes"]/div/div/div[2]/form/div[1]/input'
                    )
                    
        elem.send_keys(ano)
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
        num_processos = soup_registros.get_text().split(' ')[1]

        # Definir o numero de vezes que ira percorrer as paginas
        range_loop = int(num_processos) / 10
        range_loop = math.ceil(range_loop)

        # Print on the screen the number of pages and registers
        print(f'\nForam encontrados {num_processos} registros em {range_loop} páginas!')
        
        # Loop a ser feito nas paginas
        count = 1
        count_processos = 1
        for number in range(range_loop):

            # Pegar Conteúdo da página
            try:
                elementos = chrome.find_elements_by_class_name('publicacoes')
            except:
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
                try:
                    relator = elem.find_element(By.CLASS_NAME, 'relator')
                except:
                    relator = elem.find_element(By.CLASS_NAME, 'relator')

                text_relator = outer_html(relator)
                txt.write(text_relator + "\n")

                # Pegar a data do despacho
                try:
                    despacho = elem.find_element(
                        By.XPATH, '//*[@id="conteudo"]/div[2]/md-content/div[2]/div[1]/div[2]'
                        )
                except:
                    despacho = elem.find_element(
                    By.XPATH, '//*[@id="conteudo"]/div[2]/md-content/div[2]/div[1]/div[2]'
                    )
                text_despacho = outer_html(despacho)
                txt.write(text_despacho + "\n")

                # Pegar os dados dos envolvidos no processo
                try:
                    envolvidos = elem.find_elements(By.CLASS_NAME, 'envolvido')
                except:
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
                try:
                    shadow_root = WebElement(chrome, shadow_root_id, w3c=True)
                except:
                    shadow_root = WebElement(chrome, shadow_root_id, w3c=True)

                try:
                    content_html = shadow_root.find_elements(
                        By.TAG_NAME, 'p'
                        )
                except:
                    content_html = shadow_root.find_elements(
                        By.TAG_NAME, 'p'
                        )
                
                for conteudo in content_html:
                    # Desvio para corrigir problema de não carregar o HTML
                    texto = outer_html(conteudo)
                    # try:
                    #    html_content = conteudo.get_attribute('outerHTML')
                    # except:
                    #    html_content = conteudo.get_attribute('outerHTML')
                    # soup = BeautifulSoup(html_content, 'html.parser')
                    # texto = soup.get_text()

                    if len(texto) < 3:
                        continue
                    # método para remover o /xa0
                    novo_texto = unicodedata.normalize("NFKD", texto)
                    # pprint(texto)
                    try:
                        txt.write(texto + "\n")
                    except:
                        for x in texto:

                            if x == '\u0303' or x == '\u0301' or x == '\x96' or x == '\u0327' or x == '\u0315' \
                            or x == '\u201f' or x == '\u02da' or x == '\u0300' or x == '\u02c8' or x == '\u2215' \
                            or x == '\u25aa' or x == '\u2012' or x =='\u202f' or x == '\u0302' or x == '\u030a' \
                            or x == '\u03b2':
                                #print(x)

                            
                                continue
                            elif x == '\u2212':
                                x = '-'
                            txt.write(x)
                            

                    # print(novo_texto)
                num_processos_file.write(f'{count_processos}) <P>{text_processo} \n')
                count_processos += 1
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
            sleep(2)

    with open(caminho_resumo, "a") as resumo:
        date_hour_end = datetime.today().strftime('%d/%m/%Y %H:%M')
        second_row = f'Início: {date_hour_start}h - Término: {date_hour_end}h'
        resumo.write(second_row + '\n')
        resumo.write(f'Total de Processos: Encontrados {num_processos} registros' + '\n')
        resumo.write(f'Processos Baixados: {num_processos}' + '\n')
        resumo.write('Situação: DOWNLOAD OK')

    num_processos_file.write(f'\nNúmero de Processos = {count_processos - 1}')
    num_processos_file.close()
    chrome.close()
    print('\nPressione Ctrl + C para finalizar o programa!')

except Exception as err:
    with open(caminho_resumo, "a") as resumo:
        date_hour_end = datetime.today().strftime('%d/%m/%Y %H:%M')
        second_row = f'Início: {date_hour_start}h - Término: {date_hour_end}h'
        resumo.write(second_row + '\n')
        resumo.write(f'Total de Processos: Encontrados {num_processos} registros' + '\n')
        resumo.write(f'Processos Baixados: {count_processos - 1}' + '\n')
        resumo.write('Situação: DOWNLOAD INCOMPLETO')

    num_processos_file.write(f'\nNúmero de Processos = {count_processos - 1}')
    num_processos_file.close()
    chrome.close()
    print(err)
    print('\nPressione Ctrl + C para finalizar o programa!')
# Developed by Felipe Barreto da Silva
