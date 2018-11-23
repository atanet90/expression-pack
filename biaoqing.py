#
# Based on https://github.com/kinsluck/Biaoqingbao
#

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

HEADERS = {
    'X-Requested-With':
    'XMLHttpRequest',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer':
    "http://www.fabiaoqing.com"
}


# 创建当日表情包文件夹
def makedir():
    dirname = "scraped"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        os.chdir(dirname)
    else:
        os.chdir(dirname)


# 保存表情
def save_pic(realbq_url, bq_name):
    img = requests.get(realbq_url, headers=HEADERS, timeout=10)
    with open(bq_name, 'ab') as f:
        f.write(img.content)


# 主爬虫，获取图片url，正则匹配图片格式后缀作为文件名后缀
def crawler(url):
    r = requests.get(url, headers=HEADERS).text
    try:
        img_infos = BeautifulSoup(r, 'lxml').find('div', {
            'class': 'ui segment imghover'
        }).find_all('a')
        for img_info in img_infos:
            url_info = img_info.find('img', {'class': 'ui image lazy'})
            realbq_url = url_info['data-original']
            realbq_url = re.sub('bmiddle', 'large', realbq_url)
            bq_name = url_info['title']
            bq_name = re.sub('。|:|-|\?|/', '', bq_name).strip()
            try:
                suffix = re.search('jpg|jpeg',
                                realbq_url).group()
                bq_name += '.' + suffix
                save_pic(realbq_url, bq_name) 
            except KeyboardInterrupt:
                return
            except:
                # Ignore all errors we might encounter and keep on scraping
                pass
    except KeyboardInterrupt:
        return
    except:
        # Ignore all errors we might encounter and keep on scraping
        pass
    print(url)

def start():
    makedir()
    bq_url = [
        'http://fabiaoqing.com/biaoqing/lists/page/{cnt}.html'.format(cnt=cnt)
        for cnt in range(0, 3000)
    ]
    pool = Pool(processes=cpu_count())
    pool.map(crawler, bq_url)

if __name__ == '__main__':
    start()
