from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import pandas as pd
import time
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # ACCESSING CHROME THROUGH BINARY LOCATION
chrome_driver_path = r"C:\chromedriver_win32\chromedriver.exe" # CHROME PATH
browser = webdriver.Chrome(chrome_driver_path, options=options)



#--------------------------------------------------------------
#url='https://www.stjoeshealth.org/find-a-doctor/provider-results?RadiusDistance=%3F%20string:%20%3F&RadiusDistanceText=&OnlyAcceptingNewPatients=false&Gender=2&GenderText=Female&page=1&count=100'
#urls=browser.get(url)

f=open('Male_links.txt','a')
for i in range(16):
    i=i+1
    print(i)
    url='https://www.stjoeshealth.org/find-a-doctor/provider-results?RadiusDistance=%3F%20string:%20%3F&RadiusDistanceText=&OnlyAcceptingNewPatients=false&Gender=1&GenderText=Male&page='+str(i)+'&count=100'
    urls=browser.get(url)
    time.sleep(5)
    elems = browser.find_elements_by_xpath("//a[contains(@class,'sized')]")
    for elem in elems:
        link=elem.get_attribute("href")
        #print(link)
        f.write(str(link)+'\n')
f.close()  
print('Sucessfully completed')
