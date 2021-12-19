import requests
import os
import csv
import pickle
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from fake_useragent import UserAgent
from time import sleep

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

"""GET Request на Яндекс по URL на страницу каталога товаров, возвращает список url на товары"""
def ya_get(url):
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.927 Yowser/2.5 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
#    options.add_argument(f"--proxy-server={random.choice(proxy_bank)}")
    
    driver = webdriver.Chrome(
        executable_path=os.getcwd() + '/chromedriver.exe', 
        options=options
    )

#    driver.add_cookie({"Cookie" : "yandexuid=4770802181639543932; cmp-merge=true; reviews-merge=true; nec=0; is_gdpr=0; is_gdpr_b=COXsVhDXVigC; currentRegionId=62; currentRegionName=%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%8F%D1%80%D1%81%D0%BA; mOC=1; yuidss=4770802181639543932; ymex=1954903942.yrts.1639543942; i=UYNJKs3NIvcLpwGDiR3UIsY1nfvUqLuBoZm4EyjiChncX6ZYqhRTsbN9r8q5QxJkmJCe0XUWnXqElM2H1MBfgn/Drec=; spravka=dD0xNjM5NTQ1MjAzO2k9NDUuMTUuMTE0LjEwO0Q9RDA2Mzc4NkJGOTA1RDk0QUVBMDk2MjM1MzZCMUQ3MUZCNDU0NDU5QzQzOTVGOEYxOTczN0M4REQzNzM4OEJGQzk1MUU7dT0xNjM5NTQ1MjAzMjU0MDYzODE1O2g9MTFkZTZhYjBiMjI5NmIyOTFmYTZlYTE2OTRjYTAyZmE=; mda=0; yandex_gid=62; my=YwA=; orrXTfJaS=1; sae=0:F4FE3E33-6F31-48B3-B78D-5E23801EB56D:p:21.11.3.927:w:d:RU:20210118; gdpr=0; _ym_d=1639747957; ys=svt.1#def_bro.0#ead.2FECB7CF#wprid.1639748395248812-8464730322387522435-sas3-0995-c92-sas-l7-balancer-8080-BAL-6756#ybzcc.ru#newsca.native_cache; yabs-frequency=/5/00010000000jaxnX/oWvpS9G00010H262OK5jXW0003n48sAaGMs60000F4Gd/; skid=9205802091639748397; src-wprid=1639748395248812-8464730322387522435-sas3-0995-c92-sas-l7-balancer-8080-BAL-6756; src-utm-source-service=web; src-pof=1601; market_ys=1639748395248812-8464730322387522435-sas3-0995-c92-sas-l7-balancer-8080-BAL-6756; visits=1639543932-1639543932-1639748397; utm_campaign=ymp_brand_1_syb_search_rus; utm_term=yandex%20market; utm_medium=search; utm_source=yandex; market_cpa=1; js=1; pof=%7B%22clid%22%3A%5B%221601%22%5D%2C%22distr_type%22%3Anull%2C%22mclid%22%3Anull%2C%22opp%22%3Anull%2C%22vid%22%3Anull%7D; cpa-pof=%7B%22clid%22%3A%5B%221601%22%5D%2C%22distr_type%22%3Anull%2C%22mclid%22%3Anull%2C%22opp%22%3Anull%2C%22vid%22%3Anull%7D; dcm=1; server_request_id_market:index=1639748397765%2Ff918d828af35340f4714c5ac57d30500; ugcp=1; suppress_order_notifications=1; yp=1671079943.brd.6302000000#1671079943.cld.2270452#1640148798.mcv.0#1640148798.mct.null#1640148798.szm.1:1366x768:1366x652#1639969877.clh.2270454#1642216032.ygu.1#1639755155.gpauto.56_041862%3A92_903755%3A140%3A1%3A1639747955#1640352756.mcl.#1639834357.ln_tp.01; Polaris=0; fonts-loaded=1; _yasc=ep4x8DJHiBlWPuet3DkqHClCTGt2eSMXyuDeXuY3D99XqC8WwhzUcvgWHByB0smDygDofg==; parent_reqid_seq=1639748397765%2Ff918d828af35340f4714c5ac57d30500%2C1639748412880%2F9811cc5d8cbd6daabfb6abad57d30500"})

    try:
        driver.get(url)
        sleep(10)
        pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))
        urls_goods = ya_parse_urls(bs(driver.page_source, 'html.parser'))
    except Exception as e:
        print(e)
    finally:
        #driver.delete_all_cookies()
        driver.close()
        driver.quit()
        return urls_goods

"""Парсит html со страницы перечисления товаров, возвращает список URL на товары"""
def ya_parse_urls(bsobj):
    out_urls = list()

    try:
        url_list = bsobj.find_all('article', {'class': '_2vCnw cia-vs cia-cs'})
        for url in url_list:
            out_urls.append('https://market.yandex.ru/' + url.find('a')['href'])
    except:
        print('[INFO] BAD URL')

    return out_urls

"""Парсит страницу товара, качает картинки, заполняет csv"""
def parse_page(url):
    good_specs = list()
    photo_names = list()
    photo_urls = list()
    good_photo_urls = list()

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.927 Yowser/2.5 Safari/537.36")
#    options.add_argument(f"--proxy-server={random.choice(proxy_bank)}")
    
    driver = webdriver.Chrome(
        executable_path=os.getcwd() + '/chromedriver.exe', 
        options=options
    )
    try:
        os.mkdir('img')
    except Exception as e:
        print(e)
        pass

    try:
        driver.get(url)
        if os.path.isfile("cookies.pkl"):
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
        sleep(10)
        bsobj = bs(driver.page_source, 'html.parser')

        try:
            name = bsobj.find('h1', {'class': '_1BWd_ _2OAAC undefined'}).text
        except:
            name = 'no_data'
            print('[INFO] BAD NAME')

        try:
            dirname = ''.join(filter(str.isalnum, name))
            os.mkdir('img/' + dirname)
        except Exception as e:
            print(e)
            pass

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

    except Exception as e:
        print(e)
    finally:
        file_writer.writerow({"Наименование": name, "Цена": price, "Описание": good_specs, 
            "Производитель": customer, "Ссылка на производителя": customer_url, 
            "Ссылки на картинки": good_photo_urls, "Имена картинок": photo_names})
        driver.close()
        driver.quit()
    

if __name__ == "__main__":

    urls = ya_get(url_list)
    parse_page(urls[3])