import requests
import re

def pares_page(url):
    respone = requests.get(url)
    text = respone.text
    title = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>', text, re.DOTALL)
    time = re.findall(r'<p class="source">.*?<a .*? .*?>(.*?)</a>', text, re.DOTALL)
    auth = re.findall(r'<p class="source">.*?<a .*? .*?>.*?</a>.*?<a .*? .*?>(.*?)</a>', text, re.DOTALL)
    content_x = re.findall(r'<div class="contson" .*?>(.*?)</div>', text, re.DOTALL)
    contents = []
    pemos = []
    for content in content_x:
        xx = re.sub('<.*?>',"",content)
        contents.append(xx.strip())
    for s in zip(title,time,auth,contents):
        title, time, auth, contents = s
        pemo = {
            "title":title,
            "time":time,
            "auth":auth,
            "contents":contents
        }
        pemos.append(pemo)
    for pemo in pemos:
        print(pemo)
        print("="*50)



def main():
    url = 'https://www.gushiwen.org/default.aspx?page=1'
    pares_page(url)


if __name__ == "__main__":
    main()