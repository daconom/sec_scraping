import requests
import time
import re
import traceback
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from random import randint
from lxml import etree
from lxml.cssselect import CSSSelector

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException     
import time

browser = webdriver.Safari(executable_path = '/usr/bin/safaridriver')    
browser.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=only&accno=&start=100&count=100')
time.sleep(3)
html_all=browser.find_elements_by_xpath('/html/body/div/table[2]/tbody/tr/td[2]/a[1]')
length=len(html_all)
ofn="ussec.csv"
outFile = open(ofn, 'a', encoding='utf8')
outFile.write("cik;name;trading_symbol;address;director;officer;owner10p;other;dataofearliesttransaction;title\n")

for i in range(length):
    try:
        browser.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=only&accno=&start=100&count=100')
        if i==0:
            x=i+2
            y=x+1
        else:
            x=x+2
            y=x+1
        reporting_check=browser.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[%d]/td[3]/a' % (x)).get_attribute("innerText")
        status=reporting_check[-11:]
        print(status)
        if status=="(Reporting)": 
            browser.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[%d]/td[2]/a[1]' % (y)).click()
            time.sleep(5)
            cik_expanded=browser.find_element_by_xpath("/html/body/div[@id='contentDiv']/div[@id='filerDiv'][2]/div[@class='companyInfo']/span[@class='companyName']/a[2]").get_attribute("innerText")
            cik=cik_expanded[:10]
            print(cik_expanded)
            print(cik)
            browser.find_element_by_xpath("/html/body/div[@id='contentDiv']/div[@id='formDiv'][2]/div/table[@class='tableFile']/tbody/tr[2]/td[3]/a").click()
            time.sleep(2)
            name=browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[1]/table[1]/tbody/tr/td/a').get_attribute("innerText")
            print(name)
            trading_symbol=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[2]/span[@class='FormData']").get_attribute("innerText")
            print(trading_symbol)
            director=browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[3]/table/tbody/tr[1]/td[1]').get_attribute("innerText")
            print(director)
            officer=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[1]").get_attribute("innerText")
            print(officer)
            owner10p=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[3]/table/tbody/tr[1]/td[3]").get_attribute("innerText")
            print(owner10p)
            other=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[3]").get_attribute("innerText")
            print(other)
            if other == "X":
                specifiedposition=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[1]/td[3]/table/tbody/tr[3]/td/span[@class='FormData']").get_attribute("innerText")
                print(specifiedposition)
            dataofearliesttransaction=browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/span[@class='FormData']").get_attribute("innerText")
            print(dataofearliesttransaction)
            try:
                length_innertable=len(browser.find_elements_by_xpath("/html/body/table[3]/tbody/tr/td[1]"))
                print(length_innertable)
                for j in range(length_innertable):
                    d=j+1
                    title=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[1]").get_attribute("innerText")
                    transaction_date=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[2]").get_attribute("innerText")
                    deemed_exection_date=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[3]").get_attribute("innerText")
                    transaction_code=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[4]").get_attribute("innerText")
                    transaction_code_V=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[5]").get_attribute("innerText")
                    amount=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[6]").get_attribute("innerText")
                    A_or_D=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[7]").get_attribute("innerText")
                    price=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[8]").get_attribute("innerText")
                    beneficially_owned=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[9]").get_attribute("innerText")
                    ownership_form=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[10]").get_attribute("innerText")
                    nature_of_indirect=browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[%d]/td[11]").get_attribute("innerText")
            except:
                print("No html/body/table[3]")
                print(name)
            
            try:
                length_innertable=len(browser.find_elements_by_xpath("/html/body/table[4]/tbody/tr/td[1]"))
                print(length_innertable)
                for j in range(length_innertable):
                    d=j+i
                    title_of_derivate=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[1]" % (d)).get_attribute("innerText")
                    print(title_of_derivate)
                    conversion_or_excersice_prize=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[2]"%(d)).get_attribute("innerText")
                    transaction_date=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[3]"%(d)).get_attribute("innerText")
                    execution_date=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[4]"%(d)).get_attribute("innerText")
                    print(execution_date)
                    transaction_code=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[5]"%(d)).get_attribute("innerText")
                    print(transaction_code)
                    transaction_code_V=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[6]"%(d)).get_attribute("innerText")
                    print(transaction_code_V)
                    number_of_derivate_acquired=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[7]"%(d)).get_attribute("innerText")
                    number_of_derivate_disposed=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[8]"%(d)).get_attribute("innerText")
                    date_exe=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[9]"%(d)).get_attribute("innerText")
                    expiration_date=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[10]"%(d)).get_attribute("innerText")
                    title_underlying=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[11]"%(d)).get_attribute("innerText")
                    amount_underlying=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[12]"%(d)).get_attribute("innerText")
                    price_of_derivate_security=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[13]"%(d)).get_attribute("innerText")
                    beneficially_owned=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[14]"%(d)).get_attribute("innerText")
                    ownership_form=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[15]"%(d)).get_attribute("innerText")
                    indirect_beneficial_ownership=browser.find_element_by_xpath("/html/body/table[4]/tbody/tr[%d]/td[16]"%(d)).get_attribute("innerText")
            except:
                print("No html/body/table[4]")
    except:
        print("fail")
