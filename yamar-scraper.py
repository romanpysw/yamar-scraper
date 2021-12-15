import requests
import os
import random
import csv
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from fake_useragent import UserAgent

"""Страница с перечислением товаров"""
url_list = "https://market.yandex.ru/catalog--noutbuki-v-krasnoiarske/54544/"

"""Список прокси, нужно заполнить стабильными рабочими IP прокси"""
proxy_bank = [
#    '51.161.9.105:8080',
#    '51.161.9.105:8080'
]

wFile = open("yamar_res.csv", mode = "w", encoding = 'utf-8')
names = ["Наименование", "Цена", "Описание", 
        "Производитель", "Ссылка на производителя", 
        "Ссылки на картинки", "Имена картинок"]
file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names)
file_writer.writeheader()

"""GET Request на Яндекс по URL, возвращает html текст"""
def ya_get(url):
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument(f"--proxy-server={random.choice(proxy_bank)}")
    
    driver = webdriver.Chrome(
        executable_path=os.getcwd() + '/chromedriver.exe', 
        options=options
    )

    try:
        driver.get(url)
        return driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.delete_all_cookies()
        driver.close()
        driver.quit()

"""Парсит html со страницы перечисления товаров, возвращает список URL на товары"""
def ya_parse_urls(bsobj):
    out_urls = list()

    try:
        url_list = bsobj.find_all('article', {'class': '_2vCnw cia-vs cia-cs'})
        for url in url_list:
            out_urls.append('https://market.yandex.ru/' + url.find('a')['href'])
            print('https://market.yandex.ru/' + url.find('a')['href'])
        print(len(out_urls))
    except:
        print('[INFO] BAD URL')

    return out_urls

"""Парсит страницу товара, качает картинки, заполняет csv"""
def parse_page(bsobj):
    good_specs = list()
    photo_names = list()
    photo_urls = list()
    good_photo_urls = list()

    try:
        name = bsobj.find('h1', {'class': '_1BWd_ _2OAAC undefined'}).text
    except:
        name = 'no_data'
        print('[INFO] BAD NAME')

    try:
        price = bsobj.find('div', {'class': '_3NaXx _3kWlK'}).text
    except:
        price = 'no_data'
        print('[INFO] BAD PRICE')

    try:
        specs = bsobj.find('div', {'class': '_18fxQ'})
        for spec in specs:
            for title in spec:
                good_specs.append(title.text)
    except:
        good_specs.append('no_data')
        print('[INFO] BAD SPECS')

    try:
        customer = bsobj.find('span', {'class': 'I7X9U odzxI _3lbcP'}).text
    except:
        customer = 'no_data'
        print('[INFO] BAD CUSTOMER')
    
    try:
        customer_url = 'https://market.yandex.ru' + bsobj.find('span', {'class': 'I7X9U odzxI _3lbcP'}).find('a')['href']
    except:
        customer_url = 'no_data'
        print('[INFO] BAD CUSTOMER URL') 

    try:
        photo_urls = bsobj.find_all('li', {'class': '_2et7a'})
        dirname = ''.join(filter(str.isalnum, name))

        try:
            os.mkdir('img/' + dirname)
        except:
            pass

        for photo_url in photo_urls:
            good_photo_urls.append('https:' + photo_url.find('img')['src'][:photo_url.find('img')['src'].rfind('/')] + '/orig')
            photo_names.append(good_photo_urls[len(good_photo_urls) - 1][good_photo_urls[len(good_photo_urls) - 1].find('img_id'):-5])

            img_data = requests.get(good_photo_urls[len(good_photo_urls) - 1]).content

            with open('img/'+ dirname + '/' + photo_names[len(photo_names) - 1], 'wb') as fw:
                fw.write(img_data)

    
    except Exception as e:
        photo_urls.append('no_data')
        photo_names.append('no_data')
        print(e)
        print('[INFO] BAD PHOTOS')
    

    file_writer.writerow({"Наименование": name, "Цена": price, "Описание": good_specs, 
        "Производитель": customer, "Ссылка на производителя": customer_url, 
        "Ссылки на картинки": good_photo_urls, "Имена картинок": photo_names})
    

if __name__ == "__main__":

    parse_page(bs(ya_get(ya_parse_urls(bs(ya_get(url_list), 'html.parser'))[0]), 'html.parser'))



    """
    try:   
        os.mkdir('img/')
    except:
        pass

    with open('index.html', 'r', encoding='utf-8') as fr:
        html = fr.read()
    bsobject = bs(html, 'html.parser')
    
    parse_page(bsobject)
    

------------------------------------------------


    with open('indexlist.html', 'r', encoding='utf-8') as fr:
        html = fr.read()
    bsobject = bs(html, 'html.parser')
    ya_parse_urls(bsobject)
    """

