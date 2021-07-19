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




for i in range(1):
#----------------------Extracting Doctors Details------------------------------------------------------
    i=i+1
    #url='https://www.adventisthealthcare.com/doctors/profile/'+str(i)
    url='https://doctors.beaumont.org/search?filter=gender%3AFemale&sort=name&page=101'#+str(i) #no need to add categori use this link
    
    print(i,') URL-->',url)
    
    source_doc = requests.get(url,verify=False).text
    soup_doc = BeautifulSoup(source_doc, 'html.parser')

    #------------------------Doctor Name and Sufix---------------------------
    doc_info=soup_doc.find("div", {"data-testid":"ProviderList"})
    for doc in doc_info.find_all("div", {"data-testid":"ProviderCard"}):
        
        name_sfx=doc.find("h2", {"class":"css-1yi8h8m-ProviderName e16v8r6n5"})
        name_sfx=name_sfx.text

        if ',' not in name_sfx:
            name_sfx=name_sfx+',-'
            prit('Added - as sfx')

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
            fname=name_sfx.strip()
            mname=''
            lname=''
            sfx=''
        print('fname: '+fname+', Mname: '+mname+', Lname: '+lname)
        #print('PROVIDER SUFFIX: '+sfx)
        


        #------------------------Doctor Speciality & Gender---------------------------
        speciality=doc.find_all("div", {"class":"css-5gcvyg-SummaryColumn eeq4ow41"})[0]
        sp=[]
        for spe in speciality.find_all("li", {"class":"css-p6aqbe-SummaryColumnItem eeq4ow44"}):
            spe=spe.text
            sp.append(spe)
        
        if len(sp)==1:
            sp1=sp[0]
            sp2=''
            sp3=''
        elif len(sp)==2:
            sp1=sp[0]
            sp2=sp[1]
            sp3=''
        elif len(sp)>2:
            sp1=sp[0]
            sp2=sp[1]
            oth=",".join(sp[2:])
            sp3=oth

        #print('speciality: '+sp1)
        #print('Sub speciality: '+sp2)
        #print('Other speciality: '+sp3)
        #print('Gender: FEMALE')

        #------------------------Address---------------------------
        try:
            address=doc.find("table", {"class":"css-osr3y0-LocationTable ezmqhoo0"})

            for add in address.find_all("tr", {"class":"css-yk1mm6-LocationRow ecuprll5"}):
                test=''
                try:
                    phno=add.find("td", {"class":"css-1f7zzlc-PhoneNumberTd ecuprll8"}).text
                except:
                    phno=''
                
                grp1=add.find("strong", {"class":"css-v6mj72-LocationName ecuprll2"}).text
                grp1=grp1.strip()
        
                ad=add.find("td", {"class":"css-d83rn9-AddressTd ecuprll7"}).text
                blnc=ad.replace(grp1,'')
                
                split=blnc.split(',')
                
                state_pin=split[-1].strip()
                state=state_pin.split(' ')[0]
                pin=state_pin.split(' ')[1]
                    
                if len(split)==4:
                    add1=split[0].strip()
                    suit=split[1].strip()
                    city=split[2].strip()
                    
                elif len(split)==3:
                    add1=split[0].strip()
                    suit=''
                    city=split[1].strip()
                    
                elif len(split)==5:
                    add1=split[0].strip()
                    grp1=split[1].strip()
                    suit=split[2].strip()
                    city=split[3].strip()
                    test='address length is 5 here'
            
                else:
                    print('---------------------please check the address length is not 4, 5 or 3')
                    add1=input('please input add1 ')
                    suit=input('please input suit ')
                    city=input('please input city ')
                    state=input('please input state ')
                    pin=input('please input pin ')
                item=[url,'BHC','','','',sp1,sp2,'','',fname,mname,lname,sfx,'FEMALE','','','',grp1,add1,suit,city,state,pin,phno,test,sp3]
                lines.append(item)
                    
        except:
            add1=''
            grp1=''
            suit=''
            city=''
            pin=''
            phno=''
            test='No address for this person pleas check'
        item=[url,'BHC','','','',sp1,sp2,'','',fname,mname,lname,sfx,'FEMALE','','','',grp1,add1,suit,city,state,pin,phno,test,sp3]
        lines.append(item)

            
            
        
            
            #print('fname: '+fname+', Mname: '+mname+', Lname: '+lname)
            #print('PROVIDER SUFFIX: '+sfx)
            #print('speciality: '+sp1)
            #print('Sub speciality: '+sp2)
            #print('Other speciality: '+sp3)
            #print('Gender: FEMALE')
            #print('phno:'+phno)
            #print('Group 1:'+grp1)
            #print('Address 1:'+add1)
            #print('Suit Other address :'+suit)
            #print('City:'+city)
            #print('State:'+state)
            #print('Pin:'+pin)


            

        print('---------------------------------------------')
        
df=pd.DataFrame(lines)
df.to_csv('BeaumontHospital_FemaleData.csv', index=False)

print("Sucessfully generated output CSV")
