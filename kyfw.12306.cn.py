from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Qiangpiao(object):
    path = r'D:\chromedriver\chromedriver.exe'
    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.initmy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.driver = webdriver.Chrome(executable_path=Qiangpiao.path)
    def login(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver,1000).until(EC.url_to_be(self.initmy_url))
        print('登陆成功')
    def wait_input(self):
        self.from_station = input("出发地：")
        self.to_station = input("目的地：")
        #时间格式2018-11-26
        self.from_tiam = input("出发时间：")
        self.user = input("乘车人：")
        self.tra = input("车次:(多个车次用,隔开)").split(",")

    def order_ticke(self):
        self.driver.get('https://kyfw.12306.cn/otn/leftTicket/init')
        WebDriverWait(self.driver,1000).until(EC.text_to_be_present_in_element_value((By.ID,'fromStationText'),self.from_station))
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, 'toStationText'), self.to_station))
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, 'train_date'), self.from_tiam))
        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.ID, 'query_ticket')))
        searctBtn = self.driver.find_element_by_id('query_ticket')
        searctBtn.click()

        WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.XPATH,'//tbody[@id="queryLeftTable"]/tr')))
        tr_lists = self.driver.find_elements_by_xpath('.//table/tbody[@id="queryLeftTable"]/tr[not(@datatran)]')
        for tr in tr_lists:
            train_num = tr.find_element_by_class_name("number").text
            if train_num in self.tra:
                erdengzuo = tr.find_element_by_xpath('.//td[4]').text
                yingzuo = tr.find_element_by_xpath('.//td[10]').text
                print('二等座：',erdengzuo)
                print("硬座",yingzuo)
                if erdengzuo == "有" or erdengzuo.isdigit() or yingzuo == "有" or yingzuo.isdigit():
                    yudingBtn = tr.find_element_by_class_name('btn72')
                    yudingBtn.click()
                    WebDriverWait(self.driver,1000).until(EC.url_to_be('https://kyfw.12306.cn/otn/confirmPassenger/initDc'))
                    WebDriverWait(self.driver, 1000).until(
                    EC.presence_of_element_located((By.ID, 'normalPassenger_0')))
                    chexbox = self.driver.find_element_by_id('normalPassenger_0')
                    chexbox.click()
                    subBtn = self.driver.find_element_by_id('submitOrder_id')
                    subBtn.click()
                    WebDriverWait(self.driver,1000).until(EC.presence_of_element_located((By.CLASS_NAME, 'dhtmlx_wins_body_outer')))
                    WebDriverWait(self.driver,1000).until(
                    EC.presence_of_element_located((By.ID, 'qr_submit_id')))
                    ConBotton = self.driver.find_element_by_id('qr_submit_id')
                    ConBotton.click()
                    while ConBotton:
                        ConBotton.click()
                        ConBotton = self.driver.find_element_by_id('qr_submit_id')
                    return


    def run(self):
        self.login()
        self.wait_input()
        self.order_ticke()


if __name__ == '__main__':
    qiangpaio = Qiangpiao()
    qiangpaio.run()
