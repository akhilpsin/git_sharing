from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # ACCESSING CHROME THROUGH BINARY LOCATION
chrome_driver_path = r"C:\chromedriver_win32\chromedriver.exe" # CHROME PATH
browser = webdriver.Chrome(chrome_driver_path, options=options)

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


lines=[['URL','SUPPLY CODE','PEDIATRIC','ADJUSTMENT TYPES','EMPLOYER NAME','MAIN SPECIALTY','SUBSPECIALTY','CROSS WALK SPECIALTY','NPI',
        'PROVIDER FIRST NAME','PROVIDER MIDDLE NAME','PROVIDER LAST NAME','PROVIDER SUFFIX','GENDER','BIRTHDATE','EDUCATION YEAR (MD GRADUATION)',
        'SEARCH AGE','GROUP1','ADDRESS1','SUITE OR OTHER ADDRESS INFO1','CITY1','STATE1','ZIP1','PHONE NO 1','PHONE NO 2','OTHER SPECIALTY']]

#-Input excel file with all the address address under "SOURCE_ADDRESS" coulmn-
df = pd.read_excel('input.xlsx') # can also index sheet by name or fetch all sheets
add = df['SOURCE_ADDRESS'].tolist()
add = [x for x in add if str(x) != 'nan']



l_num=1
for i in add:
#----------------------Extracting Doctors Details------------------------------------------------------
    url=str(i)
    print(str(l_num)+')'+url)
    l_num=l_num+1
    
    #------------selenium
    urls=browser.get(url)
    time.sleep(3)
    try:
        elems = browser.find_element_by_xpath("//div[contains(@class,'col-xs-12 ih-widget-column')]")
        source_doc=elems.get_attribute('outerHTML')
        #-----------end
        
        soup_doc = BeautifulSoup(source_doc, 'html.parser')
        #print(soup_doc)

        #-----------------gender
        gen='MALE'
        #-----------------NPI
        npi=str(soup_doc).split('''"Npi":''')[1]
        npi=npi.split(''',"PatientRating"''')[0]
        #print('NPI: ',npi)

        #-----------------NPI
        name_sfx=str(soup_doc).split('''"FullName":"''')[1]
        name_sfx=name_sfx.split('''","Gender"''')[0]
        

        #------------------------Doctor Name---------------------------

        #name_sfx=soup_doc.find("h1", {"class":"mb-2"}).text
        #name_sfx=name_sfx.strip()
        
        if ',' not in name_sfx:
            name_sfx=name_sfx+',-'
            prit('Added - as sfx')
    except:
        pass

    try:
        sfx=name_sfx.split(',')[1].strip()
        name=name_sfx.split(',')[0].strip()
        name=name.split(" ")

        fname=name[0].strip()                             
        if len(name)==3:
            mname=name[1].strip()
            lname=name[2].strip()
        else:
            mname=''
            lname=name[1].strip()
    except:
        try:
            fname=name_sfx.strip()
        except:
            fname=''
        mname=''
        lname=''
        sfx=''
    #print('fname: '+fname+'\nMname: '+mname+'\nLname: '+lname)
    #print('PROVIDER SUFFIX: '+sfx)


    #------------------------Doctor Speciality---------------------------
    try:
        spe=soup_doc.find("div", {"class":"ih-tab-1 row ng-scope"})
        spe_filter=spe.find_all("li")
        spr=''
        for i in spe_filter:
            spr=spr+str(i.text)+'#'

        all_spe=spr.split('#')
            
        sp1=all_spe[0].strip()
        if len(all_spe)==2:
            sp2=all_spe[1].strip()
            sp3=''
        elif len(all_spe)>2:
            sp2=all_spe[1].strip()
            sp3=','.join(all_spe[2:])
        else:
            sp2=''
            sp3=''
    except:
        sp1=''
        sp2=''
        sp3=''
        
        
    #print('Primary Speciality: ',sp1,'\nSecondary Speciality: ',sp2,'\nOther speciality: ',sp3)

    
    #------------------------Address and phone number---------------------------
    try:

        all_address_card=soup_doc.find("div", {"class":"col-xs-12 col-md-12 location-group"})
        address_card=all_address_card.find_all("div", {"class":"location-unit"})

        for i in address_card:
            try:
                grp1=i.find("div", {"class":"form-group ih-field-locationnamelink"}).text
            except:
                grp1=''

            try:
                phno=i.find("div", {"class":"form-group ih-field-phone"}).text
                phone=phno.strip()
            except:
                phone=''

            add=i.find("div", {"class":"form-group ih-field-locationaddress"})
            add=str(add)
            add=add.replace('</div>','')
            new=add.split('<div class="">')[1]
            split=new.split('<br/>')
            #print(new)
            
            state_pin_city=split[-1].strip()
            city=state_pin_city.split(',')[0]
            state_pin=state_pin_city.split(',')[1].strip()
            state=state_pin.split(' ')[0]
            pin=state_pin.split(' ')[1]

            if len(split)==3:
                add1=split[0].strip()
                suit=split[1].strip()
                
            elif len(split)==2:
                add1=split[0].strip()
                suit=''
            else:
                add1=''
                suit=''
                
            #print('Phone: ',phone)
            #print('Group 1:'+grp1)
            #print('Address 1:'+add1)
            #print('Suit Other address :'+suit)
            #print('City:'+city)
            #print('State:'+state)
            #print('Pin:'+pin)
                
            item=[url,'SMMC','','','',sp1,sp2,'',npi,fname,mname,lname,sfx,gen,'','','',grp1,add1,suit,city,state,pin,phone,' ',sp3]
            lines.append(item)
            

            
    except:
        print('error please check')



    


df=pd.DataFrame(lines)
df.to_csv('StJoeshealth_Male_data.csv', index=False)

print("Sucessfully generated output CSV")


