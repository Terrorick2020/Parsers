from bs4 import BeautifulSoup
from time import sleep
import requests
import json

# url = input('Введите url сайта: ')
url = 'https://gpt-chatbot.ru/'
page_dict = {}
list_href = []
tags_list = ['span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'em', 'li', 'a', 'img', 'meta', 'title', 'nav', 'figcaption']
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

response = requests.get(url)
sleep(2)

with open('index_pars_bs4.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

with open('index_pars_bs4.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'lxml')

page_dict['page_title'] = soup.title.text

meta_set = set()
for tag in soup.find_all('meta'):
    for attr in tag.attrs:
        if 'description' in tag[attr]:
            meta_set.add(tag['content'])
else:
    pre_list = list(meta_set)
    page_dict['meta_desc_content'] = '     '.join(pre_list)

for tag in tags_list:
    atr_dict = {}
    index = 0
    for elem in soup.find_all(tag):
        res = ''
        try:
            if tag == 'img':
                res = elem.attrs['alt']
            elif tag in ['nav', 'meta']:
                res = elem.attrs
            elif tag == 'a':
                if 'http://' == elem.attrs['href'][:7] or 'https://' == elem.attrs['href'][:8] or elem.attrs['href'][0] == '/':
                    res = {'url': elem.attrs['href'],
                           'name': elem.get_text().strip()}
                    if res['name'] != '':
                        list_href.append(res)
            else:
                res = elem.text.strip()
            if res != '':
                atr_dict[index] = res
                index += 1
        except Exception:
            print('Error')
    page_dict[decoder_dict[tag] + tag] = atr_dict


with open('json_bs4.json', 'w', encoding='utf-8') as file:
    json.dump(page_dict, file, indent=8, ensure_ascii=False)

print(json.dumps(page_dict, ensure_ascii=False, indent=8))
print(list_href) #список страниц сайта
