# Описание

## Задача

Получение фотографий товаров с маркет плейса с описанием (название, цена, валюта, категория)

## Используемые технологии

selenium

# Принцип работы

## 1. Необходимо указать название раздела ```razdel``` и ссылку на раздел ```url```

```
razdel = 'Товары для красоты'
url = 'https://market.yandex.ru/catalog--tovary-dlia-krasoty/54438'
razdels = razdels_get(url)
```

### 1.1. Программа сканирует страницу на наличие подразделов на странице ```razdels = razdels_get(url)``` и в цикле обращается к страницам подразделов ```tovars_parse(url, razdel)```.

### 1.2. Собирает данные о товарах ```tovars_parse(url, razdel)``` и сохраняет в таблицу ```database_add(tovar_cur)```

### 1.3. После обхода всех разделов, обходит товары на выбранном разделе ```tovars_parse_01(url, razdel)```

## Для получения информации о товарах используются функции selenium

* ```tovars = driver.find_elements(By.CLASS_NAME, "_1H-VK")``` - получение всех товаров по классу ```_1H-VK``` в массив
* ```picture = tovar.find_element(By.CLASS_NAME, "w7Bf7").get_dom_attribute("src")``` получение фотографии текущего товара
* ```name = tovar.find_element(By.XPATH, ".//span[@itemprop='name']").text``` - получение название товара
* ```price = tovar.find_element(By.XPATH, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_headline-5')]").text``` - получение цены товара по наличию нескольких классов
* ```pricev = tovar.find_element(By.XPATH, ".//span[contains(@class,'ds-text_color_price-term') and contains(@class,'ds-text_typography_lead-text')]").text``` - получение валюты цены товара по наличию нескольких классов
* для прокрутки страницы с товарами (чтобы подгрузились все товары) используется скрипт перехода к низу страницы ```driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")```

## Для сохранения информации о полученных товарах используется библиотека ```psycopg2```

Для сохранения информации в таблицу необходимо подключения к базе данных PostgreSQL и таблица

```
CREATE TABLE IF NOT EXISTS public.tovars
(
    id integer NOT NULL DEFAULT nextval('tovars_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    price double precision,
    price_v character varying COLLATE pg_catalog."default",
    picture character varying COLLATE pg_catalog."default",
    razdel character varying COLLATE pg_catalog."default"
)
```

### Скрипт создавалася в образовательных целях и результаты работы используются для обучения