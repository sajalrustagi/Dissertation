# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 20:16:34 2015

@author: sajal
"""

import MySQLdb
import requests
from lxml import html
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import ctime

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver
    
    
display = Display(visible=0, size=(800, 600))
display.start()
db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()

def lookup(driver,link):
#    print "\n"
#    print link
#    print "\n"
    driver.get(link)
    try:
        driver.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"preview\"]/p")))
        try :
             link = driver.find_element_by_xpath("//*[@id=\"preview\"]/p[2]")
             html_link= link.get_attribute("innerHTML")
#             date= html_link.split("Date:")[1].split("<br>")[0][1:]
             source=html_link.split("Source:")[1].split("<br>")[0][1:]
             link = driver.find_element_by_xpath("//*[@id=\"preview\"]/p[2]/a[3]")
             link_news= link.get_attribute("href")
             while link_news[-1]=="\\" :
                 link_news[-1]=""
             domain=link_news.split("/")[2]
#             print date
#             print source
#             print link_news
#             print "\n"
             insert_query="INSERT INTO News_Sources_Disease ( Domain_Name , Full_Link , Source_Name ) Values ( \""+str(domain)+"\", \"" + str(link_news) +"\", \"" + str(source) + "\");"
             #print insert_query
             try :
               cursor.execute(insert_query)
               print insert_query
               db.commit()
             except Exception, e: 
                if str(e).find("(1062, \"Duplicate entry")==-1:
                       print str(e)
                       print "ERROR :", insert_query
                db.rollback()
             #raw_input("Press ENTER to exit")
        except :
            pass
    except TimeoutException:
        print("Box or Button not found in promedmail")

            
if __name__ == "__main__":
    print ctime()
    #print "Selenium Driver"
    driver = init_driver()
    link=[]
    domain=[]
    ask_sql="SELECT DISTINCT Article_URL from Disease_HealthMap_Full where Location like \"%India\" and Source like \"%Google%\""
    try:
       cursor.execute(ask_sql)
       results = cursor.fetchall()
       for rows in results :
           links=rows[0]
           #print "links" , links
           if links not in link : 
               link=link + [links]
               domain=domain+[links.split("/")[2]]
#               print links
#               print links.split("/")[2]
#               print "\n"
               insert_query="INSERT INTO News_Sources_Disease ( Domain_Name , Full_Link ) Values ( \""+str(links.split("/")[2])+"\", \"" + str(links) + "\");"
               #print insert_query               
               try :
                   cursor.execute(insert_query)
                   print insert_query
                   db.commit()
               except Exception, e: 
                   if str(e).find("(1062, \"Duplicate entry")==-1:
                       print str(e)
                   db.rollback()
               #raw_input("Press ENTER to exit")
               #print links
    except Exception,e :
        pass
        #print str(e)
        
#    print "Now Promed"
        
#    ask_sql_II="SELECT DISTINCT Article_URL from Disease_HealthMap_Full where Location like \"%India\" and Source like \"%Promed%\""
#    try:
#       cursor.execute(ask_sql_II)
#       results = cursor.fetchall()
#       for rows in results :
#           links=rows[0]
#           lookup(driver,links)
#    except Exception,e :
#        print str(e)
#    print
    time.sleep(5)
    driver.quit()
    db.close()
    display.stop()