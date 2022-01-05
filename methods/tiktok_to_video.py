from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request

def TiktokToVideo(message):
    driver = webdriver.Chrome("drivers/chromedriver.exe")
    link = ""
    driver.get(message.content)
    while link == "":
        try:
            link = driver.find_element(By.CSS_SELECTOR,'.tiktok-lkdalv-VideoBasic.e1yey0rl4').get_attribute('src')
        except Exception:
            link = ""
    urllib.request.urlretrieve(link, 'tiktok.mp4')