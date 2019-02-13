import requests
from lxml import etree
from urllib import request
import re
import os
import threading
from queue import Queue

class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        respons = requests.get(url,headers=self.headers,timeout=5)
        text = respons.text
        html = etree.HTML(text)
        image_urls = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        for image_url in image_urls:
            try:
                url_x = image_url.get("data-original")
                url = re.sub(r"!dta","",url_x)
                title_x = image_url.get("alt")
                title = re.sub(r"[\x08\?？,，、！!\.。~|/*]","",title_x)
                type = os.path.splitext(url)[1]
                filename = title+type
                self.img_queue.put((url,filename))
            except OSError:
                continue
            except requests.exceptions.Timeout:
                global NETWORK_STATUS
                NETWORK_STATUS = False  # 请求超时改变状态
                if NETWORK_STATUS == False:
                    for i in range(1, 10):
                        print('请求超时，第 % s次重复请求' % i)
                        respons = requests.get(url, headers=self.headers, timeout=5)
                        if respons.status_code == 200:
                            return respons


class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue


    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            url,filename = self.img_queue.get()
            request.urlretrieve(url, "images/" + filename)
            print(filename+"下载成功")

def main():
    page_queue = Queue(3000)                          #创建队列
    img_queue = Queue(1000)
    for x in range(1,2153):
        url = "http://www.doutula.com/photo/list/?page=%d" %x
        print(url)
        page_queue.put(url)                         #写入队列

    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()                                  # 启动

    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()