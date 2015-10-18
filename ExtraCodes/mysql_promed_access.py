# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:27:19 2015

@author: sajal
"""
import MySQLdb
import operator

try:
    db = MySQLdb.connect("192.168.111.195","root","sajal","Disease_names" )

except Exception, e: 
    print repr(e)

cursor = db.cursor()
ask_sql="SELECT DISEASE_NAME FROM DISEASE_INFO_FULL_MODIFY"
dict_disease_split={}
dict_bigram_trigram={}
try:
   cursor.execute(ask_sql)
   results = cursor.fetchall()
   for rows in results :
            name= rows[0]
            print name
            list_names=name.split(" ")
            for names in list_names :
                if len(names)==0:
                    del list_names[list_names.index(names)]
                else :
                    replaced_name=names.replace("," , "").replace("-" , "").replace("." , "").lower()
                    list_names[list_names.index(names)]=replaced_name
                    if replaced_name in dict_disease_split :
                        dict_disease_split[replaced_name]+=1
                    else :
                        dict_disease_split[replaced_name]=1
                    
            print list_names
   db.commit()
except Exception, e: 
    print repr(e)
    db.rollback()

sorted_dict_disease_split = sorted(dict_disease_split.items(), key=operator.itemgetter(1), reverse=True)