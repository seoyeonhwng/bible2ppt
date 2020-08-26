from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import csv

BIBLE_API = 'http://ibibles.net/quote.php?kor'
BIBLE_CHAPTER = 'http://m.ibibles.net/quote10.htm'
RESPONSIVE_READING = 'https://allneed.tistory.com/1747'


class BibleAPI():
    def get_bible(self, chapter, aa, bb, cc, dd):
        """
        인자로 들어온 해당 성경 말씀을 구하여 반환한다.

        :params: 
            * chapter (string): 성경의 챕터 
            * aa (string): 시작 장 
            * bb (string): 시작 절
            * cc (string): 끝 장 
            * dd (string): 끝 절

        :return: 
            title, sentence_list
            * title (string) : 성경 말씀 범위
            * sentence_list (list of dictionary) : 찾고자하는 성경 말씀

        """
        chapter_codes = self.__get_bible_chapter_codes()
        chapter_code = chapter_codes.get(chapter)
    
        if not chapter_code:
            print('no chapter')
            return

        headers = {'Content-Type': 'application/json'}
        res = requests.get(f'{BIBLE_API}-{chapter}/{aa}:{bb}-{cc}:{dd}', headers=headers)

        if res.status_code != 200:
            print('bible api http_request error')
            return

        body = BeautifulSoup(res.content.decode('utf-8'), 'html.parser').body.stripped_strings

        sentence_list = []
        for idx, b in enumerate(body):
            if idx % 2 == 0:
                sentence = {'section': b}
            else:
                sentence['sentence'] = b

            if sentence.get('section') and sentence.get('sentence'):
                sentence_list.append(sentence)

        return f'{chapter} {aa}:{bb}-{cc}:{dd}', sentence_list

    def get_responsive_reading(self, rr_idx):
        """
        인자로 들어온 해당 성시 교독을 반환한다.

        :params: 
            * rr_idx (string): 성시 교독 번호

        :return: 
            rr_title, rr_list
            * rr_title (string) : 성시교독 제목
            * rr_list (list of string) : 성시교독 말씀

        """
        with open('responsive_reading.csv', encoding='utf-8') as rr:
            rdr = csv.reader(rr, delimiter='|', quotechar='"')
            rr_list = []
            for r in rdr:
                if r[0] == str(rr_idx):
                    rr_title = r[1]
                    rr_list.append(r[2])

            return rr_title, rr_list

    def __get_bible_chapter_codes(self):
        with open('bible_chapter_codes.csv', encoding='utf-8') as chapter:
            rdr = csv.reader(chapter, delimiter='|', quotechar='"')
            return dict([(r[1], r[0]) for r in rdr])

    def __make_bible_chapter():
        headers = {'Content-Type': 'application/json'}
        res = requests.get(BIBLE_CHAPTER, headers=headers)

        if res.status_code != 200:
            print('make_bible_chapter error')
            return

        options = BeautifulSoup(res.content.decode('utf-8'), 'html.parser').find_all('center')[2].find_all('option')
        with open('bible_chapter_codes.csv', 'w', encoding='utf-8', newline='') as chapter:
            wr = csv.writer(chapter, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for o in options:
                wr.writerow([o.string.split(' ')[0], o.string.split(' ')[1].replace('(', '').replace(')', '')])

    def __make_responsive_reading(self):
        def __check_hangeul(s):
            # 한글이 한번이라도 사용되면 True
            regex = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
            return True if regex.findall(s) else False

        def __check_title(s):
            # 숫자 + . 의 형태가 한번이라도 사용되면 True
            regex = re.compile('[0-9][.]')
            return True if regex.findall(s) else False

        r_list = BeautifulSoup(urlopen(RESPONSIVE_READING).read(), 'html.parser').tbody.find_all('a')
        print('{} responsive_readings'.format(len(r_list)))

        with open('responsive_reading.csv', 'w', encoding='utf-8', newline='') as rr:
            wr = csv.writer(rr, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for r in r_list:
                r_idx = ''.join(i for i in r.text.split('_ ')[0] if i.isdigit())
                r_title = r.text.split('_ ')[1]
                r_link = r.get('href')

                print('writing: {} - {}'.format(r_idx, r_title))

                r_content = BeautifulSoup(urlopen(r_link).read(), 'html.parser').find_all('p', {'class': '0'})
                for c in r_content:
                    r_text = c.text
                    if not __check_hangeul(r_text) or __check_title(r_text) or r_text == '' or 'ppt' in r_text:
                        print('===> filtered: {} - {} : {}'.format(r_idx, r_title, r_text))
                        continue
                    wr.writerow([r_idx, r_title, r_text])
