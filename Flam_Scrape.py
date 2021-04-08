import selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import lxml
import csv
import pandas as pd
from openpyxl import load_workbook

PATH = "Documents\drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
pub_chem_home = "https://pubchem.ncbi.nlm.nih.gov"
goog = "https://www.google.com/"
chem_spider = "http://www.chemspider.com/"
#location = 'Desktop\flam_cas.csv'
cas_file = open('Desktop\F1CorCL2.csv', 'r') 
reader = csv.reader(cas_file)
statements = []
ids = []
y = 0

for row in reader:
    ids.append(row)

for x in ids:
    print(y/100)
    y = y+1
    if x[0] == "end":
        break

    driver.get(chem_spider) 
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=text]'))
        )
        page = driver.page_source
        page_code = BeautifulSoup(page, 'lxml') 
        driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_simple_query"]').send_keys(x[0] + Keys.ENTER) #Search from homepage

        try:
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewTabDetailsControl_prop"]').click() #Clicks on the properties tab

            item = driver.page_source
            item_soup = BeautifulSoup(item, 'lxml')
            container = item_soup.find('div', id='suppInfoTab')

            name = item_soup.find('span', id='ctl00_ctl00_ContentSection_ContentPlaceHolder1_RecordViewDetails_rptDetailsView_ctl00_WrapTitle').text
            print(name)
            x.append(name)
            """
            try:
                bp = container.find('span', text='Experimental Boiling Point:').parent.parent.parent
                print("Boiling Point = " + bp.td.text)
                x.append("Boiling Point = " + bp.td.text)

            except:
                print("boiling point error")
                x.append("boiling point error")
                pass
            """
            try:
                fp = container.find('span', text='Experimental Flash Point:').parent.parent.parent
                print("Flash Point = " + fp.td.text)
                x.append("Flash Point = " + fp.td.text)
            except:
                print("flash point error")
                x.append("flash point error")
            
        except:
            print("Page not reached")
            x.append("Page not reached")
            pass
       
    except:
        x.append("error 1")
    #print(x)
    print("")
 
driver.quit()

with open("Desktop\exceptions.csv",'w', encoding='utf-8') as data_file:
    writer = csv.writer(data_file)
    for line in ids:
        writer.writerow([line])
