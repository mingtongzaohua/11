# coding=utf-8

import requests
import re#正则表达式
import os
import urllib.request
import threading

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
        #if else 内容不可互换，记得为啥嘛？因为我理解错了
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # else:
        #     print(i)
        #     continue
        file_path = file_path + "/" + str(i + 1) + ".jpg"
        if os.path.exists(file_path):      
            continue
        pic_link = "http://fm.shiyunjj.com/" + part1 + "/" + part2 + "/" + str(i+1) + ".jpg"
        # connectWeb(file_path,pic_link,part2,i,0.1)
        myThread(i, file_path,pic_link,part2,i,0.1).start()

def connectWeb(file_path,pic_link,part2,i,t):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
        'Referer': 'http://www.mmjpg.com/mm/' + part2 + '/1'
    }
    try:
        response = requests.get(pic_link, headers=header, timeout=t)
        print('正在下载第%s张图片' % (i + 1))
        print(pic_link)
        save(file_path, response)
        print('第%s张图片下载成功！TimeOut=%f' % (i+1,t))
    except Exception as e:
        print("出现异常-->"+str(e))
        # 不必循环，超时异常但是依然可以下载成功,why?
        tt=t+t
        return connectWeb(file_path,pic_link,part2,i,tt)

class myThread (threading.Thread):
    def __init__(self, threadID,file_path,pic_link,part2,i,t):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.file_path=file_path
        self.pic_link=pic_link
        self.part2 = part2
        self.i = i
        self.t=t

    def run(self):
        print ('Starting%d' %self.threadID)
        connectWeb(self.file_path,self.pic_link,self.part2,self.i,self.t)
        print ('Exiting%d'%self.threadID)


_Url = "http://www.mmjpg.com/mm/"

for i in range(5):
    Url = _Url + str(i+1)
    path = str(i+1)
    getPicture(Url, path)
