# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 23:23:13 2015

@author: sajal
"""
from lxml import html
import time,os
import MySQLdb
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import ctime
from pyvirtualdisplay import Display



#display = Display(visible=0, size=(800, 600))
#display.start()
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()

def init_driver():
    profile = webdriver.FirefoxProfile(os.path.expanduser("/home/sajal/Desktop/Promed_scrap/Mozilla_Profile/"))
    driver = webdriver.Firefox(firefox_profile=profile) 
    driver.wait = WebDriverWait(driver, 5)
    time.sleep(5)
    return driver
 
 
def lookup(driver):
    sources=["ProMED Mail","ProMED MBDS","ProMED South Asia","ProMED Middle East"]
    for source in sources :
        sql="SELECT distinct `Article_URL` FROM `Disease_HealthMap_Full` where `Source` = \""+source+"\" ORDER BY `Disease_HealthMap_Full`.`Date` DESC"
        try :
            cursor.execute(sql)
            results = cursor.fetchall()
            for rows in results :
                url=rows[0]
                driver.get(url)
                time.sleep(10)
                try:
                    driver.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id=\"preview\"]/p[2]")))
                    
                    article = driver.find_element_by_xpath("//*[@id=\"preview\"]/p[2]")
                    text=article.get_attribute("textContent")
                    final_article= text.replace("A ProMED-mail posthttp://www.promedmail.orgProMED-mail is a program of theInternational Society for Infectious Diseaseshttp://www.isid.org","").replace("\"","'").encode("utf-8")
    #                print final_article
                    date_subject = driver.find_element_by_xpath("//*[@id=\"preview\"]/p[1]")
                    text=date_subject.get_attribute("textContent")
                    subject_split=text.split("Subject:")
                    date=subject_split[0].replace("Published Date:","")
                    subject=subject_split[1].split("Archive Number:")[0].replace("\"","'").encode("utf-8")
                    print date
                    print subject
                    insert_query="INSERT INTO `Disease_names`.`Corpus_English` (`Source`,`Date` ,`Headline` ,`Article` ,`URL`) VALUES( \""+str(source)+"\" ,STR_TO_DATE (\""+ str(date) +"\", ' %Y-%m-%d %T'),\""+str(subject[1:])+"\" ,\""+str(final_article)+"\" ,\""+str(url)+"\");"
                    try:
                       cursor.execute(insert_query)
                       db.commit()
                    except Exception, e:
                        print str(e)
                        print insert_query
                        db.rollback()
                except TimeoutException:
                    print("Box or Button not found in promedmail")
        except Exception,e :
            print str(e)
    
 
 
if __name__ == "__main__":
    print "Corpus_English"
    print ctime()
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    print 
    driver.quit()
    db.close()
#    display.stop()
#f=open("/home/sajal/Desktop/try.html","r")
#main_tree = html.fromstring( "".join(f.readlines()))
#diseases=main_tree.xpath("//*[@id=\"preview\"]/p[2]/text()")
#print diseases