import requests
from bs4 import BeautifulSoup
import json

address_head = 'https://phrase.dict.naver.com'
# initial page
req = requests.get('https://phrase.dict.naver.com/detail.nhn?bigCategoryNo=2&targetLanguage=en')

html = req.text
is_ok = req.ok
print('connected: ' + str(is_ok))
soup = BeautifulSoup(html, 'html.parser')

categories = soup.select(
    '#container > div.snb > ul > li > a'
)

all_data_dict = {}

for category in categories:
    address_tail = category.get('href')
    print('###### category name: ' + category.text.strip())
    req = requests.get(address_head + address_tail)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    mid_categories = soup.select(
        '#content > div > dl'
    )

    big_dict = {}
    middles = mid_categories[0].select('dd > span > a')

    for middle in middles:
        print('###### mid name: ' + middle.text.strip())
        print(address_head + '/' + middle.get('href'))
        mid_req = requests.get(address_head + '/' + middle.get('href'))
        mid_html = mid_req.text
        mid_soup = BeautifulSoup(mid_html, 'html.parser')

        small_category = mid_soup.select(
            '#content > div > dl.lst_sort.sort_small'
        )
        mid_dict = {}
        if len(small_category) > 0:
            smalls = mid_soup.select(
                '#content > div > dl.lst_sort.sort_small > dd > span > a'
            )
            for small in smalls:
                print('###### small name: ' + small.text.strip())
                print(address_head + '/' + small.get('href'))
                sm_req = requests.get(address_head + '/' + small.get('href'))
                sm_html = sm_req.text
                sm_soup = BeautifulSoup(sm_html, 'html.parser')

                sentences = sm_soup.select(
                    '#main_content > div.dic_cont.cont_type > ul > li > span.info_txt'
                )
                sent_list = []
                for sentence in sentences:
                    print(sentence.text.strip())
                    sent_list.append(sentence.text.strip())
                mid_dict[small.text.strip()] = sent_list
        else:
            sentences = mid_soup.select(
                '#main_content > div.dic_cont.cont_type > ul > li > span.info_txt'
            )

            sent_list = []
            for sentence in sentences:
                print(sentence.text.strip())
                sent_list.append(sentence.text.strip())
            mid_dict['no_small_category'] = sent_list
        big_dict[middle.text.strip()] = mid_dict
    all_data_dict[category.text.strip()] = big_dict

with open('data.json', 'w') as fp:
    json.dump(all_data_dict, fp)
