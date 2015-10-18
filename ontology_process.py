# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:40:38 2015

@author: sajal
"""
def isEnglish(s):
    try:
        s.decode('ascii')
    except :
        return False
    else:
        return True

import json
import ast
import requests
import MySQLdb,re,time
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()

#langs=["Hindi"]
#
#for lang in langs :
#    sql="SELECT English_Disease , "+lang+"_Disease_Google   ,"+lang+"_Disease_Shabdkosh , "+lang+"_Disease_Hinkhoj , "+lang+"_Type_Hinkhoj ,"+lang+"_Transliterate_Shabdkosh  from Disease_Ontology_Multi"
#    try:
#       cursor.execute(sql)
#       results = cursor.fetchall()
#       for rows in results :
#                list_trans=""
#                english_name=rows[0]
#                if len(re.split(",|/|\.| ",english_name))==1 :
#                    disease_name=[]
#                    for index in range(len(rows)) :
#                        if index>0 and index<3:
#                          seperate=re.split(" , |/",rows[index])
#                          #print seperate
#                          for item in seperate :
#                              if not isEnglish(item) and item not in disease_name:
#                                  disease_name=disease_name+[item]
#                        elif index==3 :
#                              seperate=re.split(" , ",rows[index])
#                              seperate_type=re.split(" , ",rows[index+1])
#                              #print seperate
#                              for index_2 in range(len(seperate)) :
#                                  item=seperate[index_2]
#                                  if item in disease_name and seperate_type[index_2]!="noun":
#                                      del disease_name[disease_name.index(item)]
#                                  elif not isEnglish(item) and seperate_type[index_2]=="noun" and item not in disease_name:
#                                      disease_name=disease_name+[item]
#                        elif index==5:
#                                main_page=requests.get("https://inputtools.google.com/request?text="+english_name+"&itc=hi-t-i0-und&num=13&cp=0&cs=0&ie=utf-8&oe=utf-8&app=demopage") 
#                                time.sleep (10)                                
#                                x=main_page.text
#                                x=json.loads(x)
#                                disease_trans=x[1][0][1][0]
#                                #print "Transliterate :",disease_trans               
#                                #
#                                seperate=re.split(" , |/",rows[index])
#                                list_trans_eng=[]
#                                for index_3 in range(len(seperate)) :
#                                    item=seperate[index_3]
#                                    if not isEnglish(item):
#                                        list_trans_eng=list_trans_eng+[item]
#                                        if index_3==0 :
#                                            list_trans=item.encode("utf-8")
#                                        else :
#                                            list_trans=list_trans+" , "+item.encode("utf-8")
#                                if disease_trans not in seperate :
#                                    if list_trans_eng==[] :
#                                       list_trans= disease_trans.encode("utf-8")
#                                    else :
#                                        list_trans=list_trans+" : "+disease_trans.encode("utf-8")
#                    disease_names_str=""
#                    for index in range(len(disease_name)) :
#                        disease=disease_name[index]
#                        if index==0 :
#                            disease_names_str=disease.encode("utf-8")
#                        else :
#                            disease_names_str=disease_names_str+" , "+disease.encode("utf-8")
#                    print disease_names_str
#                    print list_trans
#                    insert_query="INSERT INTO  `Disease_names`.`Refined_Ontology_Multi` (`English_Disease` ,`"+lang+"_Disease` , `"+lang+"_Transliterate`)VALUES (\""+english_name+"\",\""+disease_names_str.decode("utf-8") +"\",\""+list_trans.decode("utf-8") +"\");"
#                    #print insert_query
#                    try:
#                       cursor.execute(insert_query)
#                       db.commit()
#                    except Exception, e: 
#                        print insert_query
#                        print str(e)
#                        db.rollback()
#                    print "\n"
#                    
#    except Exception, e: 
#        print repr(e)
##        
langs=["Punjabi","Gujarati"]

for lang in langs :
    sql="SELECT English_Disease , "+lang+"_Disease_Google   ,"+lang+"_Disease_Shabdkosh , " + lang+"_Transliterate_Shabdkosh  from Disease_Ontology_Multi"
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for rows in results :
                list_trans=""
                english_name=rows[0]
                if len(re.split(",|/|\.| ",english_name))==1 :
                    disease_name=[]
                    for index in range(len(rows)) :
                        if index>0 and index<3:
                          seperate=re.split(" , |/",rows[index])
                          #print seperate
                          for item in seperate :
                              if not isEnglish(item) and item not in disease_name:
                                  disease_name=disease_name+[item]
                        elif index==3:
                                if lang=="Punjabi":
                                    small_lett="pa"
                                elif lang=="Gujarati" :
                                    small_lett="gu"
                                command="https://inputtools.google.com/request?text="+english_name+"&itc="+small_lett+"-t-i0-und&num=13&cp=0&cs=0&ie=utf-8&oe=utf-8&app=demopage"
                                main_page=requests.get(command)
                                print command
                                time.sleep (10)
                                x=main_page.text
                                x=json.loads(x)
                                disease_trans=x[1][0][1][0]
                                print "Transliterate :",disease_trans               
                                #
                                seperate=re.split(" , |/",rows[index])
                                list_trans_eng=[]
                                for index_3 in range(len(seperate)) :
                                    item=seperate[index_3]
                                    if not isEnglish(item):
                                        list_trans_eng=list_trans_eng+[item]
                                        if index_3==0 :
                                            list_trans=item.encode("utf-8")
                                        else :
                                            list_trans=list_trans+" , "+item.encode("utf-8")
                                if disease_trans not in seperate :
                                    if list_trans_eng==[] :
                                       list_trans= disease_trans.encode("utf-8")
                                    else :
                                        list_trans=list_trans+" : "+disease_trans.encode("utf-8")
                    print english_name
                    disease_names_str=""
                    for index in range(len(disease_name)) :
                        disease=disease_name[index]
                        if index==0 :
                            disease_names_str=disease.encode("utf-8")
                        else :
                            disease_names_str=disease_names_str+" , "+disease.encode("utf-8")
                    print disease_names_str
                    print list_trans
                    update_query="UPDATE `Disease_names`.`Refined_Ontology_Multi` SET `"+lang+"_Disease` = \""+disease_names_str.decode("utf-8")+"\" ,`"+lang+"_Transliterate` = \""+list_trans.decode("utf-8") +"\" where `English_Disease` = \""+english_name+"\";"
                    print update_query
                    try:
                       cursor.execute(update_query)
                       db.commit()
                    except Exception, e: 
                        print update_query
                        print str(e)
                        db.rollback()
                    print "\n"
                    
                    
    except Exception, e: 
        print repr(e)