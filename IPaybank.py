import io, os, time
import json
import pyautogui
# from google.cloud import vision
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from winreg import *

class AutoDownloadIpaybank:
    def __init__(self, user_name, pass_word):
        self.user_name = user_name
        self.pass_word = pass_word
        
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.runDownload()

    def timeoutToken(self,):
        while True:
            element = '//*[@id="btn-step1"]/button[2]'
    def loadCompleted(self, locator, timeout):
        """ check website load complete """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return True
        except TimeoutException:
            return False

    def clickElement(self, xpath_element):
        """ find element on website then click """
        try:
            if self.loadCompleted(xpath_element, 50):
                element = self.driver.find_element(By.XPATH, xpath_element)
                element.click()

        except NoSuchElementException:
            print("can not find element:", xpath_element)
        except Exception:
            print("can not click try perform ")
            time.sleep(10)
            # ex_element = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.XPATH, xpath_element)))
            ex_element = self.driver.find_element(By.XPATH, xpath_element)
            ActionChains(self.driver).click(ex_element).perform()

    def click_select_date(self, id_btn):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, id_btn)))
            down_arrow_btn = self.driver.find_element(By.ID, id_btn)
            down_arrow_btn.click()
            print("click:" + id_btn)
        except Exception:
            print("can't find %s, try run javaScript" % id_btn)


    # Login to Ipaybank
    def loginIpaybank(self):
        try:
            self.driver.get("https://ipay.vietinbank.vn/login")
            print("get success")
            # captcha = self.get_captcha()
            user_ele = '//*[@id="app"]/div[2]/div/div/div/div[2]/div[2]/form/div[1]/div/div/div/input'
            self.clickElement(user_ele)
            user = self.driver.find_element(By.XPATH,user_ele)
            user.clear()
            password = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div[2]/div[2]/form/div[2]/div/div/div/input')
            password.clear()
            # captcha_input = self.driver.find_element(By.CSS_SELECTOR, "input[formControlName=captcha]")
            # button = self.driver.find_element(By.XPATH, "/html/body/app-root/login-component/div/div[1]/div[2]/div[5]/button")

            user.send_keys(self.user_name)
            password.send_keys(self.pass_word)
            # button.click()

            #first login...
        except TimeoutException:
            print("Login Ipaybank timeout")
            time.sleep(5)
            return
        except:
            # time.sleep(10)
            print("has been login Ipaybank - can't find element")

    def runDownload(self):
        """ start download Ipaybank Transaction """
        self.loginIpaybank()

        print('login success..')
        card_div = '//*[@id="app"]/div[2]/div[1]/div/div[3]/div/div[2]'#click query button
        # signed = WebDriverWait(self.driver, 500000000).until(
        #     EC.visibility_of_element_located((By.XPATH, card_div))
        # )
        # ActionChains(self.driver).click(signed).perform()
        self.clickElement(card_div)
        print('card clicked')
        time.sleep(2)
        page = '//*[@id="app"]/div[2]/div[1]/div/div[3]/div[3]/div[3]/div/div[1]/div[1]'
        self.clickElement(page)
        time.sleep(2)
        _50_transaction = '//*[@id="app"]/div[2]/div[1]/div/div[3]/div[3]/div[3]/div/div[2]/div[3]'
        self.clickElement(_50_transaction)
        print('clicked pagnation')

        # search_button = '//*[@id="app"]/div[2]/div[1]/div/div[2]/div[4]/button'
        # self.clickElement(search_button)
        # print('search button clicked')
        # table_element = WebDriverWait(self.driver, 30).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, 'cms-table paragraph-2'))
        # )
        time.sleep(2)
        table_element = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div/div[3]/section/table')
        rows = table_element.find_elements(By.TAG_NAME, 'tr')
        table_data = []
        with open('extract_data.txt', mode='w', encoding='utf-8') as log_file:
            log_file.write(' ' + '\n')

        for row in rows:
            # header_rows = row.find_elements(By.TAG_NAME, "th")
            # h_row_data = [h_cell.text for h_cell in header_rows]
            # table_data.append(h_row_data)
            # with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
            #     log_file.write(' '.join(h_row_data) + '\n')

            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            table_data.append(row_data)
            with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
                log_file.write(' '.join(row_data) + '\n')
        print('extract data success...')
        time.sleep(30)
        self.runDownload()
        # self.driver.quit()

    def isLoginError(self):
        xpath_element = '//*[@id="maincontent"]/ng-component/div[1]/div/div[3]/div/div/div/app-login-form/div/div/div[4]/p'
        login_error = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_element))).text
        print("login_error", login_error)

        if login_error == 'Mã kiểm tra không chính xác. Quý khách vui lòng kiểm tra lại.':
            return True
        return False

if __name__ == "__main__":
    file_name = f'.\\setting.json'
    with open(file_name) as file:
        info = json.load(file)
    AutoDownloadIpaybank(info['USER_NAME'],info['PASSWORD'])