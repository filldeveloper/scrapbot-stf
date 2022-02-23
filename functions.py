from pprint import pprint
from bs4 import BeautifulSoup

def outer_html(html_element):
    try:
        try:
            html_content_elem = html_element.get_attribute('outerHTML')
        except:
            html_content_elem = html_element.get_attribute('outerHTML')
    except:
        try:
            html_content_elem = html_element.get_attribute('outerHTML')
        except:
            html_content_elem = html_element.get_attribute('outerHTML')
    soup_elem= BeautifulSoup(html_content_elem, 'html.parser')
    texto = soup_elem.get_text(' ')

    return texto

def day_of_week(nome_dia):
    if nome_dia == 'Sunday':
        dia_da_semana = 'Domingo'
    elif nome_dia == 'Monday':
        dia_da_semana = 'Segunda-feira'
    elif nome_dia == 'Tuesday':
        dia_da_semana = 'Terça-feira'
    elif nome_dia == 'Wednesday':
        dia_da_semana = 'Quarta-feira'
    elif nome_dia == 'Thursday':
        dia_da_semana = 'Quinta-feira'
    elif nome_dia == 'Friday':
        dia_da_semana = 'Sexta-feira'
    else:
        dia_da_semana = 'Sábado'

    return dia_da_semana

def name_month(mes):
    if mes == '01':
        nome_mes = 'Janeiro'
    elif mes == '02':
        nome_mes = 'Fevereiro'
    elif mes == '03':
        nome_mes = 'Março'
    elif mes == '04':
        nome_mes = 'Abril'
    elif mes == '05':
        nome_mes = 'Maio'
    elif mes == '06':
        nome_mes = 'Junho'
    elif mes == '07':
        nome_mes = 'Julho'
    elif mes == '08':
        nome_mes = 'Agosto'
    elif mes == '09':
        nome_mes = 'Setembro'
    elif mes == '10':
        nome_mes = 'Outubro'
    elif mes == '11':
        nome_mes = 'Novembro'
    else:
        nome_mes = 'Dezembro'

    return nome_mes
    
