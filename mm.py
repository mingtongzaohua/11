# coding=utf-8

import requests
import re
import os
import urllib.request

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
    'Referer': 'http://210.41.224.117/Login/xLogin/Login.asp'
}


def save(file_path, response):
    with open(file_path, 'wb') as f:
        f.write(response.content)
        f.close()

def getLink(page_link):
    page_html = requests.get(page_link, headers=header)
    all_pic_link = re.findall('<img src="http://fm.shiyunjj.com/([0-9]{4})/([0-9]{1,4})/([0-9]).jpg"', page_html.text, re.S)

    #title = re.findall('<h2>.*</h2>', page_html.text, re.S)

    total = re.findall('<a href="/mm/([0-9]{1,4})/([0-9]{2})">', page_html.text, re.S)

    return all_pic_link, total


def getPicture(Url, path):
    all_pic_link, total = getLink(Url)
    print(all_pic_link)
    part1 = all_pic_link[0][0]
    part2 = all_pic_link[0][1]
    

    print(part1)
    #print(title)
    print(total[0][1])

    for i in range(int(total[0][1])):
        file_path = "mm/picture/" + path

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = file_path + "/" + str(i + 1) + ".jpg"
        pic_link = "http://fm.shiyunjj.com/" + part1 + "/" + part2 + "/" + str(i+1) + ".jpg"

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
            'Referer': 'http://www.mmjpg.com/mm/' + part2 + '/1'
        }
        response = requests.get(pic_link, headers=header, timeout=0.1)

        print('正在下载第%s张图片' % (i + 1))
        print(pic_link)
        save(file_path, response)
        print('第%s张图片下载成功！' % (i+1))


Url = "http://www.mmjpg.com/mm/"

for i in range(5):
    Url = Url + str(i+1)
    path = str(i+1)
    getPicture(Url, path)
