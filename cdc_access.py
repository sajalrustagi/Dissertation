# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:56:06 2015

@author: sajal
"""

import MySQLdb,operator
try:
    db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
#dpd.cdc.gov
except Exception, e: 
    print repr(e)
cursor = db.cursor()

def delete_emergency () :
    sql="SELECT * FROM DISEASE_CDC"
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
           name=rows[0]
           link=rows[1]
           link_split=link.split("/")
           if link_split[2] =="emergency.cdc.gov":
              sql = "DELETE FROM DISEASE_CDC WHERE DISEASE_NAME = \""+ name +"\" and LINK =\""+ link +"\""
              print sql            
              try:
                   cursor.execute(sql)
                   db.commit()
              except Exception, e: 
                    print repr(e)
                    db.rollback()
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()


def update_dpd() :
    sql="SELECT * FROM DISEASE_CDC"
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
           name=rows[0]
           link=rows[1]
           #if link.find("dpd.cdc.gov")>=0:
           link_new=link.split("/")
           if link_new[2].find("dpd.cdc.gov")>=0:
              link_replaced=link.replace("dpd.","").replace("HTML/","").replace(".htm","/index.html")
              update_sql = "UPDATE DISEASE_CDC SET LINK =\""+ link_replaced +"\" WHERE DISEASE_NAME = \""+ name +"\" and LINK =\""+ link +"\""
              print update_sql            
              try:
                   cursor.execute(sql)
                   db.commit()
              except Exception, e: 
                    print repr(e)
                    db.rollback()
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()
    
def print_link2 ():
    global dic_link2
    global done_list
    sql="SELECT * FROM DISEASE_CDC"

    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
           name=rows[0]
           link=rows[2]
           #if link.find("dpd.cdc.gov")>=0:
           link_new=link.split("/")
           count_link=link_new[3]               
           if link not in done_list : 
               if count_link in dic_link2 :
                   dic_link2[count_link]=dic_link2[count_link] +1
               else :
                    dic_link2[count_link]=1
               done_list=done_list+[link]
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
           #if link.find("dpd.cdc.gov")>=0:
           link_new=link.split("/")
           count_link=link_new[3]
           extra_link=[]
           for links in link_new :
               if links!="":
                   extra_link=extra_link+[links]
           
           if dic_link2[count_link]==1 and (len(extra_link)==3 or (len(extra_link)==4 and extra_link[3].find("index") >=0)):
               type_name="Disease"
           else :
               type_name=count_link
           update_sql = "UPDATE DISEASE_CDC SET TYPE =\""+ type_name +"\" WHERE DISEASE_NAME = \""+ name +"\" and LINK =\""+ link +"\""
           #print update_sql
           try:
               cursor.execute(update_sql)
               db.commit()
           except Exception, e:
                print update_sql
                print repr(e)
                db.rollback()
               
               
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()  
    

done_list=[]
dic_link2={}
print_link2()
sorted_dic_link2 = sorted(dic_link2.items(), key=operator.itemgetter(1), reverse=True)