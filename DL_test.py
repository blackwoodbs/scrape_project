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
EDGE = "Downloads\edgedriver_win64_\msedgedriver.exe"
driver = webdriver.Chrome(PATH)
sds_db = "https://chemicalsafety.com/sds-search/"
goog = "https://www.google.com/"
sds = "http://sds.chemicalsafety.com/sds/pda/msds/getpdf.ashx?action=msdsdocument&auth=200C200C200C200C2008207A200D2078200C200C200C200C200C200C200C200C200C2008&param1=ZmRwLjFfNjgwMDc4MDNORQ==&unique=1617836424&session=7ea3a8b5502b93b997894d8692e02a56&hostname=50.238.91.150"

download_dir = "Desktop\Test_SDS"

cas_file = open('Desktop\mast.csv', 'r') 
reader = csv.reader(cas_file)

test_cas = "588-63-6" #3-PHENOXYPROPYL BROMIDE

driver.get(sds_db)

def downloader(name, wait):
    time.sleep(wait)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(wait)
    pyautogui.typewrite(name, interval=.01) # Cas - Name - Date? File Location\
    time.sleep(wait)
    pyautogui.hotkey('enter')

try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "cs_txtCas"))
    )
    cas_box = driver.find_element_by_id('cs_txtCas').send_keys(test_cas) #cas box
    supplier_box = driver.find_element_by_id('cs_txtManufact').send_keys("sigma") #manufacturer box
    search_button = driver.find_element_by_id('cs_btnSearch').click() #search button
    time.sleep(3)
    
    code = driver.page_source
    soup = BeautifulSoup(code, 'lxml')
    link_name = soup.find('div', id='cs_divResults').table.a.text
    print(link_name)

    link = driver.find_element_by_partial_link_text(link_name).click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    sds = driver.find_element_by_partial_link_text('View SDS').click()
    time.sleep(3)

    downloader(link_name, 2) #THIS WORKS SOMETIMES    .TMP FILE DOWNLOADS SOMETIMES AND I DONT KNOW WHY
    time.sleep(4)
except:
    print('failed')

driver.quit()

