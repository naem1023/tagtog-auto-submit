# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException, UnexpectedAlertPresentException

import os, sys, traceback, platform, time

import pandas as pd

from selenium.webdriver.firefox.webdriver import WebDriver


def clickNextButton(driver) -> None:
    #다음 페이지 버튼 요소 가져오기
    nextButton = driver.find_element_by_xpath("""//a[@id="submit-text"]""")    
    
    #다음 페이지 버튼 클릭
    nextButton.click()
    
    #페이지 url 저장
    print('Click!')   

def search(dirname):
    file_names = os.listdir(dirname)
    targets = []
    for file_name in file_names:
        full_filename = os.path.join(dirname, file_name)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.csv': 
            targets.append(full_filename)
    return targets

class Crawler:
    """Manage method of crawling and set environments.
    """
    def __init__(self, url, path) -> None:
        self.url = url
        self.path = path
        self.driver = self.load_chrome_driver()
        self.targets = search(path)

        self.login()
        
    def login(self) -> None:
        self.driver.get('https://www.tagtog.net/-login')
        while True:
            if input() == 'c':
                break

    def print_summary(self) -> None:
        print('='*5, "Sumamry", '='*5)
        print("Starting number of comic=", self.conf['number'])
        print("Url=",self.conf['url'])
        print("Next button type = ", self.conf['next_button'])
        print("Comic name = ", self.conf['comic_name'])

    def load_chrome_driver(self) -> WebDriver:
        platform_name = platform.system()
        if platform_name == "Windows":
            driver = webdriver.Chrome(os.path.join('chromedriver.exe'))
        elif platform_name == "Darwin":
            driver = webdriver.Chrome(os.path.join('chromedriver'))
        elif platform_name == "Linux":
            driver = webdriver.Chrome(os.path.join('chromedriver_linux64'))
        
        return driver

    def crawl(self) -> None:
        """Run cralwer
        """        
        # Load synchronized page.
        self.driver.get(self.url)

        print(f"Completely load {self.url}")

        # Save all elements of web page.
        req = self.driver.page_source

        # Craete bs4 instance.
        bs_object = BeautifulSoup(req)
        
        # Save all elements of web page removed thumbnail list.
        req = self.driver.page_source

        # Craete bs4 instance for edited page source.
        soup = BeautifulSoup(req)

        # Update number and url.
        
        files = [[pd.read_csv(file_name, encoding='utf-8'), file_name] for file_name in self.targets]

        for file in files:
            for t in file[0]['0']:
                clickNextButton(self.driver)
                textarea = self.driver.find_element_by_xpath("""//textarea[@name="textarea-inputdoc"]""")    
                textarea.send_keys(t)

                doc_name = self.driver.find_element_by_xpath("""//input[@id="doc-name-submit"]""")    
                doc_name.send_keys(file[1][2:-4])

                submit = self.driver.find_element_by_xpath("""//button[@id="submit-doc-button"]""")    
                submit.click()

                time.sleep(1.5)


crawler = Crawler('https://www.tagtog.net/jay25/Q100/pool%2F%EC%83%89%EC%86%8C%ED%8F%B0', '.\\')
crawler.crawl()