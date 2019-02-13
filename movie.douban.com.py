import requests
from lxml import etree


#豆瓣


#1.获取页面

respon = requests.get('https://movie.douban.com/cinema/nowplaying/changsha/')
text = respon.text

#2.提取数据
html = etree.HTML(text)
ul = html.xpath("//ul[@class = 'lists']")[0]
lis = ul.xpath("./li")
for li in lis:
    name = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    director = li.xpath("@data-director")[0]
    print(name,score,duration ,region,director)