# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 16:03:42 2015

@author: sajal
"""

import MySQLdb
from time import ctime
db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()
ask_sql="SELECT * FROM DISEASE_INFO_FULL_MODIFY"
ask_sql2="SELECT * FROM DISEASE_INFO_FULL_MODIFY where DISEASE_FULL like \"%Re: %\" or DISEASE_FULL like \"%RE: %\""
#truncate_sql="TRUNCATE TABLE DISEASE_INFO"
#create_sql = """CREATE TABLE DISEASE_INFO_FULL (
#         RELEASE_DATE  DATE NOT NULL,
#         DISEASE_NAME  VARCHAR(100) ,
#         DISEASE_FULL VARCHAR(500))"""
delete_sql1 = "DELETE FROM DISEASE_INFO_FULL_MODIFY WHERE DISEASE_FULL like \"%ProMED-mail Frequently Asked Questions%\" or DISEASE_FULL like \"%ProMED-mail Digests%\" or DISEASE_FULL like \"%PROMED-AHEAD:%\" "
delete_sql2 = "DELETE FROM DISEASE_INFO_FULL_MODIFY WHERE DISEASE_FULL like \"%PROMED%\""



def Ist_update() :
    try:                  
       cursor.execute(ask_sql)
       results = cursor.fetchall()
       for rows in results :
            date=rows[0]
            name=rows[1]
            full=rows[2]
            #print date,name,full
            #full_replaced=full.replace("PROMED:","").replace("PROMED-EDR:","").replace("PROMED-AHEAD-EDR:","")
#            full_replaced=full.replace("Re: ","").replace("RE: ","").replace("ProCAARE: ","").replace("VRE: ","")
#            print full_replaced
            
            disease_splitted=full.split(":")
            country_splitted=disease_splitted[0].split(" - ")
            victim_splitted=country_splitted[0].split("(")
            disease_name=victim_splitted[0]
            if name !=disease_name[1:] :
                update_sql = "UPDATE DISEASE_INFO_FULL_MODIFY SET DISEASE_NAME =\""+ disease_name[1:] +"\" , DISEASE_FULL=\""+ full +"\"  WHERE DISEASE_FULL = \""+ full +"\" and RELEASE_DATE =\""+ str(date) +"\""
                print update_sql
                #print full
                try:
                   cursor.execute(update_sql)
                   db.commit()
                except Exception, e: 
                    print "I :", repr(e)
                    delete_sql = "DELETE FROM DISEASE_INFO_FULL_MODIFY WHERE DISEASE_NAME =\""+ name +"\" and DISEASE_FULL = \""+ full +"\" and RELEASE_DATE =\""+ str(date) +"\""
                    print delete_sql
                    try:
                       cursor.execute(delete_sql)
                       db.commit()
                    except Exception, e: 
                        print "II :",repr(e)
                        db.rollback()
                    
                    db.rollback()
##       print cursor.execute(delete_sql2)
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()
        
    

def IInd_update() :
    try:                  
       cursor.execute(ask_sql)
       results = cursor.fetchall()
       count=0
       for rows in results :
            date=rows[0]
            full=rows[2]
            if full.find(":")>=0 or full.find(" - ")>=0 :
                count +=1 
            else :
                update_dist=full.find("update")
                if update_dist>0:
                    full_replaced=full[0:update_dist-1]+":"+full[update_dist-1:]
                    disease_splitted=full_replaced.split(":")
                    country_splitted=disease_splitted[0].split(" - ")
                    victim_splitted=country_splitted[0].split("(")
                    disease_name=victim_splitted[0]
                    sql="UPDATE DISEASE_INFO_FULL_MODIFY SET DISEASE_NAME =\""+ disease_name[1:] +"\" , DISEASE_FULL=\""+ full_replaced +"\"  WHERE DISEASE_FULL = \""+ full +"\" and RELEASE_DATE =\""+ str(date) +"\""
                    print sql
                else :
                    sql = "DELETE FROM DISEASE_INFO_FULL_MODIFY WHERE DISEASE_FULL = \""+ full +"\" and RELEASE_DATE =\""+ str(date) +"\""
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
        
    
def IIIrd_update() :
    try:                  
       cursor.execute(ask_sql)
       results = cursor.fetchall()
       for rows in results :
            date=rows[0]
            name=rows[1]
            full=rows[2]
            if name.lower().find("update")>=0:
                update_dist=full.lower().find("update")
                if update_dist>=0:
                    full_replaced=full[0:update_dist-1]+":"+full[update_dist-1:]
                    disease_splitted=full_replaced.split(":")
                    country_splitted=disease_splitted[0].split(" - ")
                    victim_splitted=country_splitted[0].split("(")
                    disease_name=victim_splitted[0]
                    sql="UPDATE DISEASE_INFO_FULL_MODIFY SET DISEASE_NAME =\""+ disease_name[1:] +"\" , DISEASE_FULL=\""+ full_replaced +"\"  WHERE DISEASE_FULL = \""+ full +"\" and RELEASE_DATE =\""+ str(date) +"\""
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
        
    
    
#ask_sql="SELECT count(*) FROM DISEASE_INFO_FULL_MODIFY"
#cursor.execute(ask_sql)
#results = cursor.fetchall()
#for rows in results :
#   count= rows[0]
#   print rows
#
#ask_sql1="SELECT * FROM DISEASE_INFO_FULL_MODIFY LIMIT "+str(count)+","+str(count)
#print ask_sql1
#cursor.execute(ask_sql1)
#results = cursor.fetchall()
#for rows in results :
#   print rows
print "Promed_Update"
print ctime()
Ist_update()
IInd_update()
IIIrd_update()
db.close()
print