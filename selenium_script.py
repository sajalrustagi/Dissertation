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



display = Display(visible=0, size=(800, 600))
display.start()
db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()
#create_sql = """CREATE TABLE DISEASES (
#         RELEASE_DATE  DATE NOT NULL,
#         DISEASE_NAME  VARCHAR(100))"""
#cursor.execute(create_sql)
#db.close()
 
def init_driver():
    profile = webdriver.FirefoxProfile(os.path.expanduser("/home/sajal/Desktop/Promed_scrap/Mozilla_Profile/"))
    driver = webdriver.Firefox(firefox_profile=profile) 
#    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    time.sleep(2)
    return driver
 
#from selenium.common.exceptions import ElementNotVisibleException
 
def lookup(driver):
    driver.get("http://www.promedmail.org/")
    tryingwhole=True
    counterror=0
    while tryingwhole :
        try:
            driver.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id=\"latest_list\"]")))
            count=1
            
            trying=True
            while(trying) :
                try :
                    #print"reached here"
                    link = driver.find_element_by_xpath("//*[@id=\"latest_list\"]/ul/li["+str(count)+"]")
                    date=link.get_attribute("innerHTML").split("<a")[0]
                    link = driver.find_element_by_xpath("//*[@id=\"latest_list\"]/ul/li["+str(count)+"]/a")
                    text=link.get_attribute("text")
                    #print date
                    date_str=datetime.datetime.strptime(date, '%d %b %Y ').strftime('%d/%m/%Y')
                    
                    #print date_str
                    disease_splitted=text.split(":")
                    country_splitted=disease_splitted[0].split(" - ")
                    victim_splitted=country_splitted[0].split("(")
                    disease_name=victim_splitted[0]
                    full_replaced=text
                    if disease_name.lower().find("update")>=0:
                        update_dist=text.lower().find("update")
                        if update_dist>=0:
                            full_replaced=text[0:update_dist-1]+":"+text[update_dist-1:]
                            disease_splitted=full_replaced.split(":")
                            country_splitted=disease_splitted[0].split(" - ")
                            victim_splitted=country_splitted[0].split("(")
                            disease_name=victim_splitted[0]
                    #print disease_name[1:]
                    insert_query="INSERT INTO DISEASE_INFO_FULL_MODIFY (RELEASE_DATE, DISEASE_NAME,DISEASE_FULL) VALUES( STR_TO_DATE (\""+ str(date_str) +"\", '%Y-%m-%d %r'),\""+str(disease_name[1:])+"\" ,\""+full_replaced+"\");"
                    
                    try:
                       # Execute the SQL command
                       cursor.execute(insert_query)
                       print insert_query
                       # Commit your changes in the database
                       db.commit()
                    except Exception, e: 
                        counterror+=1
                        if counterror>3 :
                            return
                        #print repr(e)
                       # Rollback in case there is any error
                        db.rollback()
#                    if count==5 :
#                        trying=False
#                        tryingwhole=False
                    count+=1
                except Exception ,e :
                    print "error I :",str(e)
                    
                    trying=False
            if counterror>3 :
                     return
            button = driver.wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "prev_or_next")))
            try:
              button.click()
              print "button clicked "
              time.sleep(3)
            except :
                print "not found to click"
                tryingwhole=False
        except TimeoutException:
            print("Box or Button not found in promedmail")
            tryingwhole=False
 
 
if __name__ == "__main__":
    print "Selenium Driver"
    print ctime()
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    print 
    driver.quit()
    db.close()
    display.stop()