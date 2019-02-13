from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import re,time


class LagouSpider(object):
    path = r'D:\chromedriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.path)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='

    def run(self):
        self.driver.get(self.url)
        while True:
            WebDriverWait(driver=self.driver, timeout=20).until(
                EC.presence_of_all_elements_located((By.XPATH,'//div[@class="pager_container"]/span[last()]')))
            source = self.driver.page_source
            self.parse_list_page(source)
            next_but = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            if 'pager_next pager_next_disabled' in next_but.get_attribute("class"):                                  #判断是否到了最后一页
                break
            else:
                time.sleep(2)
                next_but.click()

    def parse_list_page(self,source):                                                                                #获取页面中职位详情链接
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(2)
    def request_detail_page(self,url):                                                                               #解析职位详情
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to_window(self.driver.window_handles[1])
        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def parse_detail_page(self,source):
        html = etree.HTML(source)
        company = html.xpath('//div[@class="company"]/text()')[0]
        position_name = html.xpath('//span[@class="name"]/text()')[0]
        job_wage = html.xpath('//span[@class="salary"]/text()')[0].strip()
        job_city = html.xpath('//dd[@class="job_request"]/p/span/text()')[1].strip()
        job_city = re.sub(r'[\s/]', '', job_city)
        job_years = html.xpath('//dd[@class="job_request"]/p/span/text()')[2].strip()
        job_years = re.sub(r'[\s/]', '', job_years)
        record = html.xpath('//dd[@class="job_request"]/p/span/text()')[3].strip()
        record = re.sub(r'[\s/]', '', record)
        content = "".join(html.xpath('//div[@class="job-detail"]/p/text()')).strip()
        job = {
            'company': company,
            'position_name': position_name,
            'job_wage': job_wage,
            'job_city': job_city,
            'job_years': job_years,
            'record': record,
            'content': content
        }
        print(job)
        print("="*50)

if __name__ == '__main__':
    LaGou = LagouSpider()
    LaGou.run()

