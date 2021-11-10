# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException, UnexpectedAlertPresentException

import os, sys, traceback, platform, time

import pandas as pd

from selenium.webdriver.firefox.webdriver import WebDriver


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
    def __init__(self, targets) -> None:
        self.targets = targets
        self.driver = self.load_chrome_driver()

        self.login()
        
    def login(self) -> None:
        self.driver.get('https://www.tagtog.net/-login')
        while True:
            if input() == 'c':
                break

    def load_chrome_driver(self) -> WebDriver:
        platform_name = platform.system()
        if platform_name == "Windows":
            driver = webdriver.Chrome(os.path.join('chromedriver.exe'))
        elif platform_name == "Darwin":
            driver = webdriver.Chrome(os.path.join('chromedriver'))
        elif platform_name == "Linux":
            driver = webdriver.Chrome(os.path.join('chromedriver_linux64'))
        
        return driver

    def crawl(self):
        for target in self.targets:
            self._crawl(target[0], target[1])
            time.sleep(4)

    def _crawl(self, url, file_name) -> None:
        """Run cralwer
        """        
        # Load synchronized page.
        self.driver.get(url)

        print(f"Completely load {url}")

        # Save all elements of web page.
        req = self.driver.page_source

        # Craete bs4 instance.
        bs_object = BeautifulSoup(req)
        
        # Save all elements of web page removed thumbnail list.
        req = self.driver.page_source

        # Craete bs4 instance for edited page source.
        soup = BeautifulSoup(req)

        # Update number and url.
        
        file = pd.read_csv(file_name, encoding='utf-8')

        for t in file['0']:
            nextButton = self.driver.find_element_by_xpath("""//a[@id="submit-text"]""")    
            nextButton.click()

            textarea = self.driver.find_element_by_xpath("""//textarea[@name="textarea-inputdoc"]""")    
            textarea.send_keys(t)

            time.sleep(0.5)

            doc_name = self.driver.find_element_by_xpath("""//input[@id="doc-name-submit"]""")    
            doc_name.send_keys(file_name[:-4])

            submit = self.driver.find_element_by_xpath("""//button[@id="submit-doc-button"]""")    
            submit.click()

            time.sleep(1.8)

targets = [
    ['https://www.tagtog.net/jay25/Q100/pool%2F%EC%A0%84%EA%B8%B0%20%EA%B8%B0%ED%83%80', '전기 기타.csv'],
    ['https://www.tagtog.net/jay25/Q100/pool%2F%EC%B2%BC%EB%A1%9C', '첼로.csv'],
    ['https://www.tagtog.net/jay25/Q100/pool%2F%EC%BD%98%ED%8A%B8%EB%9D%BC%EB%B2%A0%EC%9D%B4%EC%8A%A4', '콘트라베이스.csv']
]

crawler = Crawler(targets)
crawler.crawl()