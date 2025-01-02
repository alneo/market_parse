"""
Объяснение:
Импортируем необходимые модули: selenium для работы с WebDriver и By для поиска элементов на странице.
Указываем путь к драйверу WebDriver: Замените /path/to/chromedriver на фактический путь к файлу ChromeDriver (или другому драйверу, если вы используете другой браузер).
Создаем экземпляр WebDriver: webdriver.Chrome(driver_path) инициализирует экземпляр ChromeDriver.
Открываем страницу: driver.get(url) открывает указанную URL в браузере.
Получаем данные:
driver.find_element(By.TAG_NAME, "h1").text находит первый элемент с тегом <h1> и возвращает его текст.
driver.find_elements(By.TAG_NAME, "p") находит все элементы с тегом <p> и возвращает список этих элементов. Затем мы перебираем этот список и выводим текст каждого параграфа.
Закрываем WebDriver: driver.quit() закрывает браузер и завершает сеанс WebDriver.
Важно:
Убедитесь, что у вас установлен драйвер WebDriver для вашего браузера.
Вы можете использовать другие методы поиска элементов (например, By.ID, By.CLASS_NAME, By.XPATH) в зависимости от структуры страницы.
Обратите внимание на условия использования сайта и политику конфиденциальности перед автоматическим сбором данных.
Дополнительные возможности:
Selenium позволяет выполнять действия на странице, такие как клики, заполнение форм и прокрутка.
Вы можете использовать библиотеки для обработки данных, такие как BeautifulSoup, чтобы извлечь информацию из HTML-кода страницы.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
import hashlib
import psycopg2
import unicodedata
import re
import os
from time import sleep

DB_name = "market_tovars1"
DB_user = "postgres"
DB_pass = ""
DB_host = "127.0.0.1"
DB_port = "5433"

def razdels_get(url):
    """
    Получение ссылок с страницы и возвращение массива ссылок с именами
    """
    driver = webdriver.Chrome()
    driver.get(url)
    links_j = []
    try:
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
    except(NoSuchElementException):
        # print('NoSuchElementException')
        pass

    driver.quit()
    return links_j

def download_image(url, dir=""):
    """Скачивает изображение по URL и сохраняет его в файл.

  Args:
      url: URL изображения для скачивания.
      filename: Имя файла для сохранения изображения.

  Returns:
      None
  """
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос прошел успешно
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    dir_cur = 'tovars/'+dir
    if not os.path.exists(dir_cur):
        os.makedirs(dir_cur)
    fpath = dir_cur+'/'+filename+'.jpg'
    with open(fpath, 'wb') as f:
        f.write(response.content)
    return filename+'.jpg'

def database_add(tovar):
    """CREATE TABLE public.tovars (
        id serial NOT NULL,
        "name" varchar NULL,
        price double precision NULL,
        price_v varchar NULL,
        picture varchar NULL
    );
    ALTER TABLE public.tovars ADD razdel varchar NULL;
"""
    conn = psycopg2.connect(dbname=DB_name, user=DB_user, password=DB_pass, host=DB_host, port=DB_port)
    cur = conn.cursor()
    try:
        name = tovar['name']
        cleaned_price = 0
        # Удаляем все символы форматирования (включая "thin space")
        try:
            cleaned_price = ''.join(c for c in unicodedata.normalize('NFKD', tovar['price']) if unicodedata.category(c) != 'Cf')
            cleaned_price = re.sub(r'\s|\u2009', '', cleaned_price)
        except (Exception) as error:
            #print(error)
            pass
        price = float(cleaned_price)
        pricev = tovar['pricev']
        picture_path = tovar['picture_path']
        razdel = tovar['razdel']
        # print(tovar)
        # print(f"price:{price}; pricev:{pricev}; razdel:{razdel}; name:{name}")
        insert_query = "INSERT INTO public.tovars(name, price, price_v, picture, razdel) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(insert_query, (name, price, pricev, picture_path, razdel))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        #print(error)
        pass
    finally:
        if conn is not None:
            cur.close()
            conn.close()
        pass


def tovars_parse(url, razdel):
    driver = webdriver.Chrome()
    for i in range(1, 50):
        driver.get(url+str(i))
        tovars = driver.find_elements(By.CLASS_NAME, "_1H-VK")
        for tovar in tovars:
            try:
                picture = tovar.find_element(By.CLASS_NAME, "w7Bf7").get_dom_attribute("src")
                picture_path = download_image(picture, razdel)
                name = tovar.find_element(By.XPATH, ".//span[@itemprop='name']").text
                price = tovar.find_element(By.XPATH, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_headline-5')]").text
                pricev = tovar.find_element(By.XPATH, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_lead-text')]").text
                tovar_cur = {
                    'picture_path': picture_path,
                    'name': name,
                    'price': price,
                    'pricev': pricev,
                    'razdel': razdel
                }
                #print(tovar_cur)
                database_add(tovar_cur)
            except(NoSuchElementException):
                #print('No such element')
                pass

    driver.quit()


def tovar_get_price(tovar,xpath):
    value = ''
    try:
        value = tovar.find_element(By.XPATH, xpath).text
    except(NoSuchElementException):
        pass
    return value


def tovars_parse_01(url, razdel):
    driver = webdriver.Chrome()
    driver.get(url)
    for i in range(1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    tovars = driver.find_elements(By.CLASS_NAME, "_1H-VK")
    for tovar in tovars:
        try:
            picture = tovar.find_element(By.CLASS_NAME, "w7Bf7").get_dom_attribute("src")
            if picture is not None:
                picture_path = download_image(picture, razdel)
                name = tovar.find_element(By.XPATH, ".//span[@itemprop='name']").text
                price = 0
                pricev = ''
                tmp = tovar_get_price(tovar, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_lead-text')]")
                if tmp != '':
                    price = tmp
                tmp = tovar_get_price(tovar, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_text')]")
                if tmp != '':
                    pricev = tmp
                if price == 0 or price == '₽':
                    tmp = tovar_get_price(tovar,".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_text')]")
                    if tmp != '':
                        price = tmp
                if pricev == '':
                    tmp = tovar_get_price(tovar,".//span[contains(@class,'ds-text_text_tight') and contains(@class,'ds-text_typography_text')]")
                    if tmp != '':
                        pricev = tmp
                if price == '₽':
                    price = 0
                tovar_cur = {
                    'picture_path': picture_path,
                    'name': name,
                    'price': price,
                    'pricev': pricev,
                    'razdel': razdel
                }
                #print(tovar_cur)
                database_add(tovar_cur)
        except(NoSuchElementException):
            print('No such element')
            pass

    driver.quit()


# - https://market.yandex.ru/catalog--produkty-napitki/54434
# Всё для дома - https://market.yandex.ru/catalog--tovary-dlia-doma/54422
# Все для детей - https://market.yandex.ru/special/kids_dep
# razdel = 'Все для детей'
# url = 'https://market.yandex.ru/special/kids_dep'
razdel = 'Товары для красоты'
url = 'https://market.yandex.ru/catalog--tovary-dlia-krasoty/54438'
razdels = razdels_get(url)

for razdel_cur in razdels:
    url = razdel_cur['href']+'/?ds=1&page='
    razdel = razdel_cur['name']
    print(razdel+" : "+url)
    tovars_parse(url, razdel)

tovars_parse_01(url, razdel)