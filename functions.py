from pprint import pprint
from bs4 import BeautifulSoup

def outer_html(html_element):
    html_content_elem = html_element.get_attribute('outerHTML')
    soup_elem= BeautifulSoup(html_content_elem, 'html.parser')
    texto = soup_elem.get_text(' ')

    return texto