from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium_stealth import stealth
from time import sleep
import json

# url = input('Введите url сайта: ')

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('disable-infobars')
options.add_argument(f'user-agent={ua.random}')
options.add_argument('--headless')

proxy = "124.220.157.80:80"
webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": proxy,
   "ftpProxy": proxy,
   "sslProxy": proxy,
   "noProxy": None,
   "proxyType": "MANUAL",
   "class": "org.openqa.selenium.Proxy",
   "autodetect": False
}\

page_dict = {}
url = 'https://gpt-chatbot.ru/'
tags_list = ['span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'li', 'a', 'img', 'meta', 'title', 'nav', 'figcaption', ]
decoder_dict = {'span': 'Группировка: ',
                'h1': 'Заголовок: ',
                'h2': 'Заголовок: ',
                'h3': 'Заголовок: ',
                'h4': 'Заголовок: ',
                'h5': 'Заголовок: ',
                'h6': 'Заголовок: ',
                'p': 'Параграф: ',
                'strong': 'Важная фраза: ',
                'em': 'Важная фраза: ',
                'li': 'Строка списка: ',
                'a': 'Гиперссылка: ',
                'img': 'Изображение: ',
                'meta': 'Метаданные: ',
                'title': 'Заголовок: ',
                'nav': 'Секция: ',
                'figcaption': 'Подпись к изображению: '}

with webdriver.Chrome(options=options) as browser:
    stealth(
        browser,
        languages=['en', 'en-US', 'ru'],
        vendor='Google Inc.',
        platform='Win32',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True
    )

    browser.get(url)
    wait = WebDriverWait(browser, 10,  poll_frequency=0.1)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == "complete")
    # sleep(20)

    page_dict['page_title'] = browser.title

    meta_desc_content = ''
    for attr in browser.find_elements(By.XPATH, '//meta[@*="description"]'):
        meta_desc_content += attr.get_attribute('content') + '      '
    page_dict['meta_desc_content'] = meta_desc_content.strip()

    for tag in tags_list:
        List = browser.find_elements(By.TAG_NAME, tag)
        atr_dict = {}
        index = 0
        for atr in List:
            res = ''
            try:
                if tag == 'img':
                    res = atr.get_attribute('alt')
                elif tag in ['nav', 'meta']:
                    res = attrs_nav = browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', atr)
                else:
                    res = atr.text.strip()
                if res != '':
                    atr_dict[index] = res
                    index += 1
            except Exception:
                print('Error')
        page_dict[decoder_dict[tag] + tag] = atr_dict

with open('json_sel.json', 'w', encoding='utf-8') as file:
    json.dump(page_dict, file, indent=8, ensure_ascii=False)

print(json.dumps(page_dict, ensure_ascii=False, indent=8))
