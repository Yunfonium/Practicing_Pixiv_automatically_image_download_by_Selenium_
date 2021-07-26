import os,re,urllib.request,time,requests,threading
import keyboard
from getpass import getpass
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class PixivUser():
        def __init__(self,user,pw,driver):
                self.user = user
                self.pw = pw
                self.header = None
                self.works_links = []
                self.images_list = [] #會存取二維陣列，每[i]項內容依序為：張數、作品連結。
                self.thread_num = 100
                self.driver = driver
                self.cookies = {}
                self.main_window = None
                self.file_path = "pixiv_picture"
        def login(self):
                #開網頁
                print('Open Pixiv...')
                self.driver.get('https://www.pixiv.net/bookmark_new_illust.php') 
                
                #選擇要登入 
                time.sleep(3)
                print('Select to login...')
                button = self.driver.find_element_by_class_name("signup-form__submit--login")
                button.click()

                #打帳密
                print('input User and Password...')
                currURL = self.driver.current_url
                time.sleep(5)
                textbox = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
                textbox.send_keys(self.user)
                time.sleep(5)
                textbox = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
                textbox.send_keys(self.pw)

                #按確定
                time.sleep(5)
                print('input completely and login...')
                button = self.driver.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')
                button.click()
                time.sleep(4)
                if self.driver.current_url == currURL:
                #可能會有recaptcha，提醒使用者手動完成驗證再繼續下面步驟。
                        try:
                                recaptcha = self.driver.find_elements(By.XPATH,"/html/head/title")
                                if recaptcha != []:
                                        Ok = input("There 's a recaptcha! You should finish it and type enter here")
                                button.click()
                        except:
                                print("No recaptcha!")
                        

        def search_the_page(self): #以後會加入指定頁數的argument

                                #該頁圖片連結弄成list，注意！(By.CLASS_NAME,"classname")這一定要括號起來！
                works = self.driver.find_elements_by_xpath("//*[@id=\"js-mount-point-latest-following\"]/div/div/figure/div/a[@class = \"PKslhVT\"]/child::*")
                block = [1,""]
                for work in works:
                        if work.text:
                                block[0] = int(work.text)
                                # self.images_list[i][j] = int(work.text)
                        else:
                                style = work.get_attribute("style")
                                l = style.split()
                                url = l[-1][5:-3]
                                url = url.replace("c/240x240/img-master","img-original")
                                url = url.replace("_master1200","")
                                block[1] = url
                                self.images_list.append(block)
                                block = [1,""]
                print("searching complete")
        
        def download_original_images(self):
                print("start downloading")
                if not os.path.isdir(self.file_path):
                        os.mkdir(self.file_path)
                for image in self.images_list:
                        number = image[0]
                        href = image[1]
                        if number == 1:
                                r = requests.get(href,headers = {"Referer": "https://www.pixiv.net/","User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"})
                                if r.status_code != 200:
                                        href = href.replace("jpg","png")
                                        r = requests.get(href,headers = {"Referer": "https://www.pixiv.net/","User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"})
                                        if r.status_code != 200:
                                                continue
                                        else:
                                                self.download_image(r,href)

                                else:
                                        self.download_image(r,href)
                        else:
                                for i in range(number):
                                        page = "p"+ str(i)
                                        src = href.replace("p0",page)
                                        r = requests.get(src,headers = {"Referer": "https://www.pixiv.net/","User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"})
                                        if r.status_code != 200:
                                                src = src.replace("jpg","png")
                                                r = requests.get(src,headers = {"Referer": "https://www.pixiv.net/","User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"})
                                                if r.status_code != 200:
                                                        continue      
                                                else:
                                                        self.download_image(r,src)
                                        else:
                                                self.download_image(r,src)

        def download_image(self,request,href):
                srcString = href.split("/")
                image_name = srcString[-1]
                with open('pixiv_picture/'+image_name,"wb") as f:
                        f.write(request.content)
                print(image_name , "...OK")
                
if __name__ == "__main__":
        load_dotenv()   #先讀取.env

        # newUser = PixivUser(os.getenv("TrueUser"),os.getenv("TruePw"),driver = Chrome())  #建立User
        newUser = PixivUser(os.getenv("PixivUser"),os.getenv("PixivPw"),driver = Chrome())
        actions = ActionChains(newUser.driver)
        newUser.login()
        newUser.search_the_page()
        newUser.download_original_images()
        print("All tasks complete!")
        newUser.driver.close()