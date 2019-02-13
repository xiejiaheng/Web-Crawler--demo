import requests
from lxml import etree
from urllib import request
import threading
from queue import Queue
import csv
class Producer(threading.Thread):
    headers = {
                  "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                  "Connection": "close"
    }
    def __init__(self,Movies_url,Movies,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.Movies_url = Movies_url
        self.Movies = Movies


    def run(self):
        while True:
            if self.Movies_url.empty():
                print('没有了')
                break
            url = self.Movies_url.get()
            self.parse_page(url)
            print("保存完成：%s" %url)


    def parse_page(self,url):
        response = requests.get(url,headers=self.headers,timeout=5)
        text = response.content.decode("gb18030")
        html = etree.HTML(text)
        a = html.xpath('//a[@class="ulink"]/@href')
        for url_a in a:
            url = "https://www.dy2018.com"+url_a
            self.movies(url)

    def movies(self,url):
        proxies = {'http': '111.177.163.126:9999'
                   }
        response = requests.get(url, headers=self.headers,proxies=proxies,timeout=5)
        text = response.content.decode("gb18030")
        html = etree.HTML(text)
        movie_info = html.xpath('//div[@id="Zoom"]//text()')
        movie = {}
        for s in movie_info:
            if s.startswith("◎译　　名"):
                s = s.replace("◎译　　名", "").strip()
                movie["china_name"] = s
            elif s.startswith("◎片　　名"):
                s = s.replace("◎片　　名", "").strip()
                movie["name"] = s
            elif s.startswith("◎年　　代"):
                s = s.replace("◎年　　代", "").strip()
                movie["year"] = s
            elif s.startswith("◎产　　地"):
                s = s.replace("◎产　　地", "").strip()
                movie["origin"] = s
            elif s.startswith("◎类　　别"):
                s = s.replace("◎类　　别", "").strip()
                movie["type"] = s
            elif s.startswith("◎字　　幕"):
                s = s.replace("◎字　　幕", "").strip()
                movie["language"] = s
            elif s.startswith("◎豆瓣评分"):
                s = s.replace("◎豆瓣评分", "").strip()
                movie["score"] = s
            try:
                movie["download1"] = html.xpath('//td[@bgcolor="#fdfddf"]/a/text()')[0]
                movie["download2"] = html.xpath('//td[@bgcolor="#fdfddf"]/a/text()')[1]
            except:
                continue
        self.Movies.put(movie)

class Consumer(threading.Thread):
    headers = {
                  "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                  "Connection": "close"
    }
    def __init__(self,Movies_url,Movies,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.Movies_url = Movies_url
        self.Movies = Movies

    def run(self):
        headers = ['china_name', 'name', 'year','origin','type','language','score','download1','download2']
        while True:
            mov = self.Movies.get()
            fp = open('dytt3.csv', 'a', newline='', encoding='utf-8')
            writer = csv.DictWriter(fp, headers)
            writer.writerow(mov)
            print('保存成功！！！！')

def main():
    Movies_url = Queue(500)
    Movies = Queue(10000)

    for x in range(201,303):
        if x == 1:
            url = "https://www.dy2018.com/html/gndy/dyzz/index.html"
            Movies_url.put(url)
            print(url)
        else:
            url = "https://www.dy2018.com/html/gndy/dyzz/index_%d.html" %x
            print(url)
            Movies_url.put(url)


    for x in range(4):
        t = Producer(Movies_url,Movies)
        t.start()

    for x in range(4):
        t = Consumer(Movies_url,Movies)
        t.start()

if __name__ == '__main__':
    main()