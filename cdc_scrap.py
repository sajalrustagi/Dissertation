# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 12:02:42 2015

@author: sajal
"""
from lxml import html
import requests
from lxml import etree
import string
import MySQLdb
from time import ctime

create_sql = """CREATE TABLE DISEASE_CDC (
         DISEASE_NAME  VARCHAR(100) NOT NULL UNIQUE,
         LINK VARCHAR(500) NOT NULL)"""
try:
    db = MySQLdb.connect("localhost","root","sajal","Disease_names" )

except Exception, e: 
    print repr(e)
    
cursor = db.cursor()
link_dict={}
def dict_other_name() :
    global link_dict
    sql="SELECT * FROM disease_name_cdc"
    link_dict={}
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
           name=rows[0]
           link=rows[2]
           if link in link_dict :
               link_dict[link]=link_dict[link]+[name]
           else :
               link_dict[link]=[name]
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()
    
    
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
           name=rows[0]
           link=rows[2]
           other_names=rows[3]
           new_other_names=str(link_dict[link])[1:-1].replace("\"","'")
           if other_names != new_other_names:
               update_sql = "UPDATE disease_name_cdc SET OTHER_NAMES =\""+ new_other_names +"\" , NUMBER_NAMES = "+ str(len(link_dict[link])) +" WHERE DISEASE_NAME = \""+ name +"\" and LINK =\""+ link +"\""
               
               try:
                   
                   cursor.execute(update_sql)
                   print update_sql
                   db.commit()
               except Exception, e:
                    print repr(e)
                    db.rollback()
       db.commit()
    except Exception, e: 
        print repr(e)
        print update_sql
        db.rollback()

def scrap_cdc() :
    for i in list(string.ascii_lowercase):
        #print i
        main_page=requests.get('http://www.cdc.gov/DiseasesConditions/az/'+i+'.html')
        main_tree = html.fromstring(main_page.text)
        diseases=main_tree.xpath("//*[@id=\"AZ-content\"]/div/div/ul/li/a")
        #diseases=main_tree.xpath("//*[@id=\"anch_110\"]/text()")
        for index in range(len(diseases)):
            full=etree.tostring(main_tree.xpath("//*[@id=\"AZ-content\"]/div/div/ul/li/a")[index])
            #print full[:-2]
            start=full.find("\">")
            end=full.find("</a>")
            uptil_now =full[start+2:end].replace("&#8212;","-").replace("<em>","").replace("</em>","").replace("&amp;","and").replace("&#226;&#128;&#153;","'").replace("&#195;&#179;","o")
            see_split=uptil_now.split(" - see")[0]
            bracket_split=see_split.split(" (")[0]
            disease_name=bracket_split.split(" [")[0].replace("see also ","")
            #print square_split
            start=full.find("href=\"")
            end=full.find("\">")
            link =full[start+6:end]
            #print link
            insert_query="INSERT INTO disease_name_cdc (DISEASE_NAME,LINK) VALUES( \""+str(disease_name)+"\" ,\""+link+"\");"
            e=""
            try:
               cursor.execute(insert_query)
               db.commit()
            except Exception, e: 
                db.rollback() 
                #print str(e)
                #print insert_query
            if str(e).find("(1062, \"Duplicate entry")==-1:
                print insert_query
                print str(e)
                

print ctime()                
scrap_cdc()
dict_other_name()
db.close()
print

                    

