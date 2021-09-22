from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import chromedriver_autoinstaller
import sys
import json
import os
from urllib import request
import time

def crawl(search_term, name):

    # check the chrome browser version which is installed
    chrome_version = chromedriver_autoinstaller.get_chrome_version()
    ver = chrome_version.split('.')[0]

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    try:
        driver = webdriver.Chrome(f'./{ver}/chromedriver.exe', options=options)
    except:
        print("Auto install start")
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{ver}/chromedriver.exe', options=options)

    driver.implicitly_wait(10)
    driver.get('https://www.google.com/imghp?hl=ko&ogbl')
    elem = driver.find_element_by_name("q")

    if not os.path.isdir(name):
        os.makedirs(name, exist_ok=True)

    elem.send_keys(search_term)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        
        last_height = new_height

    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    count = 1
    for image in images:
        try:
            image.click()
            time.sleep(SCROLL_PAUSE_TIME)
            
            imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute("src")
            request.urlretrieve(imgUrl, os.path.join(name, str(count)+".jpg"))
            count = count + 1
        except :
            pass

    driver.close()

def main():
    search_terms = ["러블리즈 미주", "러블리즈 베이비소울", "러블리즈 수정", "러블리즈 예인", "러블리즈 지수", "러블리즈 지애", "러블리즈 진", "러블리즈 케이"]
    names = ['mijoo', 'babysoul', 'sujeong', 'yein', 'jisoo', 'jiae', 'jin', 'kei']

    for search_term, name in zip(search_terms, names):
        crawl(search_term, name)
    
if __name__ == '__main__':
    main()


