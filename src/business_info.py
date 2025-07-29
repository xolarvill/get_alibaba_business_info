# -*- coding: utf-8 -*-

from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import re
import time
from lxml import etree
import csv
import os

# Chrome驱动类
class Chrome_drive():
    def __init__(self):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        NoImage = {"profile.managed_default_content_settings.images": 2}  # 控制 没有图片
        option.add_experimental_option("prefs", NoImage)
        # option.add_argument('--headless')  #无头模式 不弹出浏览器
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
        })  #去掉selenium的驱动设置

        self.browser.set_window_size(1200,768)
        self.wait = WebDriverWait(self.browser, 12)

    def get_login(self):
        url='https://passport.alibaba.com/icbu_login.htm'
        self.browser.get(url)
        #这里进行人工登陆。
        k = input("请登录阿里巴巴账号，登录成功后输入1继续：\n>")
        if 'Your Alibaba.com account is temporarily unavailable' in self.browser.page_source:
            self.browser.close()
        while k == 1:
            break
        self.browser.refresh()  # 刷新方法 refres
        return

    #获取判断网页文本的内容：
    def index_page(self, page, wd):
        """
        抓取索引页
        :param page: 页码
        """
        print('正在爬取第', page, '页')

        url = f'https://www.alibaba.com/trade/search?page={page}&keyword={wd}&f1=y&indexArea=company_en&viewType=L&n=38'
        js1 = f" window.open('{url}')"  # 执行打开新的标签页
        print(url)
        self.browser.execute_script(js1)  # 打开新的网页标签
        self.browser.switch_to.window(self.browser.window_handles[-1])  # 此行代码用来定位当前页面窗口
        self.buffer()  # 网页滑动  成功切换
        
        # 等待元素加载出来
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J-items-content')))
        #获取网页的源代码
        html = self.browser.page_source

        self.get_products(wd, html)

        self.close_window()

    def buffer(self): #滑动网页的
        """Scrolls down the page to ensure all lazy-loaded content is present."""
        print("Scrolling page to load all content...")
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        scroll_wait = WebDriverWait(self.browser, 5) # 5 second timeout for each scroll increment

        while True:
            # Scroll down to the bottom of the page
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load by checking if the page height has increased
            try:
                scroll_wait.until(
                    lambda driver: driver.execute_script("return document.body.scrollHeight") > last_height
                )
                # Update height for the next iteration
                last_height = self.browser.execute_script("return document.body.scrollHeight")
            except TimeoutException:
                # If the height doesn't increase after a scroll, we've reached the end.
                print("Reached the end of the page.")
                break

    def close_window(self):
        length=self.browser.window_handles
        if len(length) > 3:
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.close()
            time.sleep(1)
            self.browser.switch_to.window(self.browser.window_handles[-1])

    def get_products(self, wd, html_text):
        """
        提取商品数据
        """
        e = etree.HTML(html_text)
        items = e.xpath('//div[@id="J-items-content"]//div[@class="item-main"]')
        print('公司数 ', len(items))
        for li in items:
            company_name = ''.join(li.xpath('./div[@class="top"]//h2[@class="title ellipsis"]/a/text()'))  # 公司名称
            company_phone_page = ''.join(li.xpath('./div[@class="top"]//a[@class="cd"]/@href'))  # 公司电话连接
            product = ''.join(li.xpath('.//div[@class="value ellipsis ph"]/text()'))  # 主要产品
            Attrs = li.xpath('.//div[@class="attrs"]//span[@class="ellipsis search"]/text()')
            length = len(Attrs)
            counctry = ''
            total_evenue = ''
            sell_adress = ''
            product_img = ''
            if length > 0:
                counctry = ''.join(Attrs[0])  # 国家
            if length > 1:
                total_evenue = ''.join(Attrs[1])  # Total 收入
            if length > 2:
                sell_adress = ''.join(Attrs[2])  # 主要销售地
            if length > 3:
                sell_adress += '、' + ''.join(Attrs[3])  # 主要销售地
            if length > 4:
                sell_adress += '、' + ''.join(Attrs[4])  # 主要销售地
            product_img_list = li.xpath('.//div[@class="product"]/div/a/img/@src')
            if len(product_img_list) > 0:
                product_img = ','.join(product_img_list)  # 产品图片
            self.browser.get(company_phone_page)
            phone = ''
            address = ''
            mobilePhone = ''
            try:
                if 'Your Alibaba.com account is temporarily unavailable' in self.browser.page_source:
                    self.browser.close()
                self.browser.find_element_by_xpath('//div[@class="sens-mask"]/a').click()
                phone = ''.join(re.findall('Telephone:</th><td>(.*?)</td>', self.browser.page_source, re.S))
                mobilePhone = ''.join(re.findall('Mobile Phone:</th><td>(.*?)</td>', self.browser.page_source, re.S))
                address = ''.join(re.findall('Address:</th><td>(.*?)</td>', self.browser.page_source, re.S))
            except:
                print("该公司没有电话")
            all_down = [wd, company_name, company_phone_page, product, counctry, phone, mobilePhone, address,
                        total_evenue, sell_adress, product_img]
            save_csv(all_down)
            print(company_name, company_phone_page, product, counctry, phone, mobilePhone, address, total_evenue,
                  sell_adress, product_img)

# 保存CSV文件
def save_csv(lise_line):
    csv_file_path = "./alibaba_com_img.csv"
    file = csv.writer(open(csv_file_path, 'a', newline="", encoding="utf-8"))
    file.writerow(lise_line)

# 主函数，获取商家信息
def get_business_info(keyword='henan', pages=31):
    """
    获取阿里巴巴国际站商家信息
    
    参数:
    keyword - 搜索关键词，默认为'henan'
    pages - 爬取页数，默认为31页
    """
    # 确保downloads_picture目录存在
    if not os.path.exists("./downloads_picture"):
        os.makedirs("./downloads_picture")
        
    # 创建CSV文件标题
    csv_title = 'wd,company_name,company_phone_page,product,counctry,phone,mobilePhone,address,total_evenue,sell_adress,product_img'.split(',')
    save_csv(csv_title)
    
    # 初始化Chrome驱动并登录
    run = Chrome_drive()
    run.get_login() # 先登录
    
    # 爬取每一页
    for i in range(1, pages):
        run.index_page(i, keyword)
    
    print(f"商家信息已保存到 alibaba_com_img.csv 文件中")
    return True