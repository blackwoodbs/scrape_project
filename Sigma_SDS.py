#sigma scrape

import selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from bs4 import BeautifulSoup
import lxml
import csv
import pandas as pd
from openpyxl import load_workbook
import pyautogui

PATH = "Documents\drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
Sigma_Home = "https://www.sigmaaldrich.com/catalog/product/aldrich/442534?lang=en&region=US&utm_medium=cpc&utm_source=bing&utm_term=aigma&utm_campaign=Aldrich%20Position%20Support%20Global%20(Bing%20ebizpfs)&utm_content=aldrich/442534"

Acetone = "67-64-1"
test = "93-97-0"

cas_file = open("Desktop\master.csv", 'r') 
reader = csv.reader(cas_file)
#statements = []
ids = []

for row in reader:
    ids.append(row)

for x in ids:

    if x[0] == "end":
        break

    driver.get(Sigma_Home)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'Query'))
            )
        driver.find_element_by_id('Query').send_keys(x[0] + Keys.ENTER)
        
        sds = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'msdsBulletPoint')))
        name = driver.find_element_by_class_name('name').text
        print(name)
        pyautogui.moveTo(500, 850).click()
        time.sleep(5)
        sds.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'msdsContentDiv')))
        pyautogui.click(500,750)
        pyautogui.click(500,850)
        pyautogui.click(button='right')
        time.sleep(5)
        pyautogui.click(550,860)
        time.sleep(5)
        pyautogui.typewrite(x[0] +" "+ name, interval=.02)
        pyautogui.hotkey('enter')
        time.sleep(2)
        
    except:
        with open("Desktop\error_collection.csv",'w') as data_file:
            writer = csv.writer(data_file)
            for line in ids:
                writer.writerow([line])
        pass

    #driver.get(Sigma_Home)

driver.quit()
