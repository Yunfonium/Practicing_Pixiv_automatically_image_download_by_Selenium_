import os 
import unittest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#先讀取.env
load_dotenv()

#建立User
test = unittest.TestCase
class PixivUser():

    User = os.getenv('PixivUser')
    Pw = os.getenv('PixivPw')
    driverpath = os.getenv('chromeDriver')

#開網頁
print('Open Pixiv...')
driver = Chrome(PixivUser.driverpath)
driver.get('https://www.pixiv.net/bookmark_new_illust.php')

#選擇要登入
print('Select to login...')
button = driver.find_element_by_class_name("signup-form__submit--login")
button.click()

#打帳密
print('input User and Password...')
textbox = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
textbox.send_keys(PixivUser.User)
textbox = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
textbox.send_keys(PixivUser.Pw)

#按確定
print('input completely and login...')
button = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')
button.click()

print('Welcome!')

