import requests
from lxml import etree

#电影天堂


BASE_URL = 'https://www.dytt8.net'
defult_url = []

#获取页面中电影的详情链接
def get_details_url(url):
    respon = requests.get(url)
    text = respon.text
    html = etree.HTML(text)
    all_a = html.xpath("//div[@class='co_content8']//a[@class='ulink']")
    for a in all_a:
        ul = a.xpath("@href")[0]
        url = BASE_URL + ul
        defult_url.append(url)
    return defult_url

#获取详情页的内容
def movie_info(url):
    movie = {}
    respon = requests.get(url)
    text = respon.content.decode('gbk')
    html = etree.HTML(text)
    movie['title'] = html.xpath("//font[@color='#07519a']/text()")[0]
    movie_info = html.xpath("//div[@id='Zoom']//text()")
    for s in movie_info:
        if s.startswith("◎年　　代"):
            s = s.replace("◎年　　代","").strip()
            movie["year"] = s
        elif s.startswith("◎产　　地"):
              s = s.replace("◎产　　地","").strip()
              movie["origin"] = s
        elif s.startswith("◎类　　别"):
              s = s.replace("◎类　　别","").strip()
              movie["type"] = s
        elif s.startswith("◎字　　幕"):
              s = s.replace("◎字　　幕","").strip()
              movie["language"] = s
        elif s.startswith("◎豆瓣评分"):
              s = s.replace("◎豆瓣评分","").strip()
              movie["score"] = s
    return movie


def movie_list():
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'     #获取1-7页的链接
    for x in range(1,8):
        url = base_url.format(x)
        movie_url = get_details_url(url)
    for url in movie_url:                                                 #获取每一页中电影详情
        movies = movie_info(url)
        print(movies)

if __name__ == '__main__':
    movie_list()