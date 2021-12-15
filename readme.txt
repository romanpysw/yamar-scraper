Язык: Python
Библиотеки: Selenium, BeautifulSoup4, fake_useragent, requests, csv, re, os, random
Дополнительно: chromedriver.exe

Суть подхода к GET запросам на яндекс маркет:
    Необходимо заполнить proxy_bank стабильными рабочими прокси,
    чем больше, тем лучше. Каждый GET запрос на яндекс маркет
    реализуется со случайным user-agent и случайным IP.
    Случайность IP реализуется за счёт рандомного выбора прокси сервера 
    из proxy_bank.