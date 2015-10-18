# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 23:29:17 2015

@author: sajal
"""
import MySQLdb,re
try:
    db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
except Exception, e: 
    print repr(e)

cursor = db.cursor()
#sql="SELECT distinct Disease FROM Disease_incidents_India"
#disease_idsp=[]
#list_remove=[" ","."]
#try:
#   cursor.execute(sql)
#   results = cursor.fetchall()
#   for rows in results :
#            disease_name=' '.join(rows[0].split())
#            while disease_name[0] in list_remove:
#                disease_name=disease_name[1:]
#            #disease_name=rows[0]
#            if disease_name not in disease_idsp :
#                disease_idsp=disease_idsp+[disease_name]
#except Exception, e: 
#    print repr(e)
#
#print disease_idsp

sql="SELECT  Disease,count(*) FROM `Disease_HealthMap_without` WHERE  `Location` LIKE  \"%india\" and Date > '2014-01-01' Group By Disease"
disease_healthmap=[]
count_healthmap=[]
#list_remove=[" ","."]
try:
   cursor.execute(sql)
   results = cursor.fetchall()
   for rows in results :
#            disease_name=' '.join(rows[0].split())
#            while disease_name[0] in list_remove:
#                disease_name=disease_name[1:]
            disease_name=rows[0]
#            if disease_name not in disease_idsp :
            disease_healthmap=disease_healthmap+[disease_name]
            count_healthmap=count_healthmap+[rows[1]]
except Exception, e: 
    print repr(e)

#print disease_healthmap
#
try:
    db1 = MySQLdb.connect("192.168.111.105","root","dhavalpatel","newsdata" )
except Exception, e: 
    print repr(e)

cursor1 = db1.cursor()

list_db=['local_information_repository','local_information_repository_dup_4','local_information_repository_dup_5','local_information_repository_dup_6' 
,'local_news_info_dup','local_news_info_dup_1','local_news_info_dup_2','local_news_info_dup_3']
#select_query=""
#for index in range(len(list_db)) :
#    sql="SELECT * FROM "+ list_db[index]
#    if index!=0 :
#        select_query=select_query +" UNION " + sql
#    else :
#        select_query=sql
#        
#print select_query
for index in range(len(disease_healthmap)) :
    diseases=disease_healthmap[index]
    count_healthmap_disease=count_healthmap[index]
    disease_small=diseases.lower()
    print disease_small
    print
    list_ids=[]
    dict_count={}
    count=0
    for dbs in list_db :
#        print dbs 
        sql="SELECT ID FROM "+ dbs +" where newsHeadline like \"% " + disease_small +" %\"" +" or newsHeadline like \"" + disease_small +" %\"" +" or newsHeadline like \"% " + disease_small +"\""
            
        try:
           print sql
           cursor1.execute(sql)
           results = cursor1.fetchall()
           for rows in results :
                    id_row=int(rows[0])
                    if id_row not in list_ids :
                        list_ids=list_ids+[id_row]
                        count+=1
#                    else :
#                        print "error repeat ",id_row,dbs
                            
        except Exception, e: 
            print repr(e)
    disease_small_split=disease_small.replace("-"," ").replace("and"," ").replace("and"," ").replace("/"," ").replace(","," ")
    disease_small_split=disease_small_split.split()
    for diseases_split in disease_small_split :
        count_split=0
        for dbs in list_db :
#        print dbs 
            #sql="SELECT count(*) FROM "+ dbs +" where newsHeadline like \"%" + diseases_split +"%\""
            sql="SELECT Count(*) FROM "+ dbs +" where newsHeadline like \"% " + diseases_split +" %\"" +" or newsHeadline like \"" + diseases_split +" %\"" +" or newsHeadline like \"% " + diseases_split +"\""
            try:
               print sql
               cursor1.execute(sql)
               results = cursor1.fetchall()
               print results
               count_split+=int(results[0][0])
                        
    #                    else :
    #                        print "error repeat ",id_row,dbs
                                
            except Exception, e: 
                print repr(e)
        print count_split
        dict_count[diseases_split]=count_split
    insert_query="INSERT INTO  Count_Healthmap_News_India (`Disease` ,`Count_News` ,`Count_HealthMap` ,`Disease_Part` ,`IDs`)VALUES ( \""+disease_small+"\", " + str(count) +", " + str(count_healthmap_disease) +  ", \"" + str(dict_count)[1:-1] + "\", \"" + str(list_ids)[1:-1] + "\");"

    #insert_query="INSERT INTO Disease_Healthmap_News_India (`Disease` ,`Count` ,`IDs`) Values ( \""+disease_small+"\", " + str(count) + ", \"" + str(list_ids)[1:-1] + "\");"
    print insert_query
    try:
       cursor.execute(insert_query)
       db.commit()
    except Exception, e: 
        print repr(e)
        db.rollback()
    print







#combine_sql="create view combined_2_ID as SELECT ID FROM local_information_repository UNION SELECT ID FROM local_information_repository_dup_4"
#try:
#   cursor1.execute(combine_sql)
#   db1.commit()
#except Exception, e: 
#    print repr(e)
#    db1.rollback()
#
#sql= "SELECT count(ID) from combined_2_ID"
#try:
#   cursor1.execute(sql)
#   results = cursor1.fetchall()
#   for rows in results :
#            print rows[0]
#except Exception, e: 
#    print repr(e)