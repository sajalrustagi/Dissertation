# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:47:27 2015

@author: sajal
"""


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
 
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
 
def lookup(driver):
    driver.get("http://www.google.com/inputtools/try/")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "demobox")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, "gt-sl")))
        button.click()
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, ":df")))
        button.click()
        box = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "democontainer")))
        
        box.send_keys("sajal".decode("utf-8"))
        box.send_keys(" ".decode("utf-8"))
#       
    except TimeoutException:
        print("Box or Button not found in google.com")
 

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    driver.quit()