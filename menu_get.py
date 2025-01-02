from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def razdels_get():
    driver = webdriver.Chrome()
    driver.get("https://market.yandex.ru/catalog--produkty-napitki/54434")
    links_j = []
    links = driver.find_elements(By.CLASS_NAME, "_3tza_._1MOwX._2eMnU.AH9fe._1gtHy._1O1a7")
    for link in links:
        href = ''
        name = link.find_element(By.CLASS_NAME, "_2SUA6.jM85b._13aK2._1A5yJ").text
        try:
            link_element = link.find_element(By.CLASS_NAME, "EQlfk")
            href = link_element.get_attribute("href")
            links_j.append({"href": href, "name": name})
        except(NoSuchElementException):
            #print('NoSuchElementException')
            pass
        #print(f"Ссылка: {href}, Текст: {name}")
    print(links_j)
    driver.quit()