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

cas_file = open("Desktop\exceptions.csv", 'r') 
reader = csv.reader(cas_file)
statements = []
ids = []

for row in reader:
    ids.append(row)

for x in ids:
    if x[0] == "end":
        break

    driver.get(pub_chem_home)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "main-content"))
        ) 
        driver.find_element(By.CSS_SELECTOR, 'input[type=text]').send_keys(x[0] + Keys.ENTER) #Compound Name/CAS # as a variable
        driver.implicitly_wait(5) 
        driver.find_element_by_xpath('//*[@id="collection-results-container"]/div/div/div[2]/ul/li/div/div/div[1]/div[1]/a').click()
        print("there was a result")
        try:
            
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Information-Sources"))
            )
            #print("there was a GHS-Classification")
            source_code = driver.page_source
            ghs_soup = BeautifulSoup(source_code, "lxml")
            compound = ghs_soup.title.text.split('|')[0]
            print(compound)
            x.append(compound)
            #x.append("GHS-Classification Section ID Located")
            ghs_info = ghs_soup.find(id="GHS-Classification")
            print("ghs classification section was found")
            ghs_hazards = ghs_info.find(class_="fixed-layout")
            hnums = ghs_hazards.find_all('tr')[2]
            for hazards in hnums('p'):
                x.append(hazards.text.split(':')[0])
        except:
            x.append("H# not found")
    except:
        x.append("No TOP RESULT on PubChem")
        driver.get(pub_chem_home)
    print(x)
    print("")
 
driver.quit()

#print(ids)


with open("Desktop\error_collection.csv",'w') as data_file:
    writer = csv.writer(data_file)
    for line in ids:
        writer.writerow([line])
