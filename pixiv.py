import os 
import unittest
import time
from getpass import getpass
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PixivUser():
    def __init__(self,user,pw,drivepath):
        self.user = user
        self.pw = pw
        self.driverpath = drivepath

#先讀取.env
load_dotenv()

#建立User
test = unittest.TestCase

newUser = PixivUser(user = os.getenv("PixivUser"),pw = os.getenv("PixivPw"),drivepath = os.getenv("chromeDriver"))


#開網頁
print('Open Pixiv...')
driver = Chrome(newUser.driverpath)
driver.get('https://www.pixiv.net/bookmark_new_illust.php')

#選擇要登入
print('Select to login...')
button = driver.find_element_by_class_name("signup-form__submit--login")
button.click()

#打帳密
print('input User and Password...')
textbox = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
textbox.send_keys(newUser.user)
textbox = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
textbox.send_keys(newUser.pw)

#按確定
print('input completely and login...')
button = driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')
button.click()

print('Welcome!')
#把圖片瀏覽網頁變成original window，因為等下要
print('正在設定本分頁為主分頁')
origin = driver.current_window_handle

#該頁圖片連結弄成list，注意！(By.CLASS_NAME,"classname")這一定要括號起來！
element = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"PKslhVT")))
imageList = driver.find_elements_by_class_name("PKslhVT")


#開第二分頁進入第一張圖的網頁，這個是用直接輸入javascript指令打開分頁的。
i = 0
href = imageList[i].get_attribute("href")
print (href)
driver.execute_script("window.open();")
driver.switch_to.window(driver.window_handles[1])
driver.get(href)

#結束關視窗
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.close()



