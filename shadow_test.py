from selenium import webdriver
from selenium.webdriver.common.by import By

def test_recommended_code():
    """Please use this code."""

    url = 'http://watir.com/examples/shadow_dom.html'

    chrome = webdriver.Chrome("/home/serpro/development/google-sheet/Google-sheet/chromedriver")
    chrome.get(url)
    

    shadow_host = chrome.find_element(By.CSS_SELECTOR, '#shadow_host')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '#shadow_content')

    assert shadow_content.text == 'some text'

    chrome.quit()

senhor = test_recommended_code()