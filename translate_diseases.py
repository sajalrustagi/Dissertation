# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:26:02 2015

@author: sajal
"""
import MySQLdb,time
from lxml import html
import requests , re
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()
import goslate
gs = goslate.Goslate()


sql="SELECT distinct Disease from Count_Distinct_Healthmap_News_India"
disease_name=[]
try:
   cursor.execute(sql)
   results = cursor.fetchall()
   for rows in results :
            disease_name=disease_name+[rows[0]]
            #print rows[0]
except Exception, e: 
    print repr(e)

"""
#############################################   hindi translate  ################################
for disease in disease_name :
    disease_hindi=gs.translate(disease, 'hi')
    print disease_hindi
    insert_query="INSERT INTO  `Disease_names`.`Disease_Ontology_Multi` (`English_Disease` ,`Hindi_Disease_Google`)VALUES (\""+disease+"\",\""+disease_hindi +"\");"
    #print insert_query
    try:
       cursor.execute(insert_query)
       db.commit()
    except Exception, e: 
        print insert_query
        print str(e)
        db.rollback()
    time.sleep(3)
    #break


#############################################   punjabi translate  ################################
for disease in disease_name :
    disease_punjabi=gs.translate(disease, 'pa')
    print disease_punjabi
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Punjabi_Disease_Google =\""+ disease_punjabi +"\"   WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    time.sleep(3)
#    break

#############################################   gujarati translate  ################################
    
for disease in disease_name :
    disease_gujarati=gs.translate(disease, 'gu')
    print disease_gujarati
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Gujarati_Disease_Google =\""+ disease_gujarati +"\"   WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    time.sleep(3)
    


#############################################   hindi translate  shabdkosh ################################

for disease in disease_name :
    print "disease :",disease
    main_page=requests.get('http://www.shabdkosh.com/hi/translate?e='+disease+'&l=hi')
    main_tree = html.fromstring(main_page.text)
    transliterated_name=""
    names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
    disease_name_lang=""
    if names==[] :
        disease_split=re.split("/|\|,| ",disease)
        if len(disease_split)>1:
            for splitted in disease_split:
                print splitted
                time.sleep(3)
                main_page=requests.get('http://www.shabdkosh.com/hi/translate?e='+splitted+'&l=hi')
                main_tree = html.fromstring(main_page.text)
                
                names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                if names==[] :
                    if "-" in splitted :
                        disease_split_again=re.split("-",splitted)
                        for splitted_again in disease_split_again:
                            print splitted_again
                            main_page=requests.get('http://www.shabdkosh.com/hi/translate?e='+splitted_again+'&l=hi')
                            main_tree = html.fromstring(main_page.text)
                            time.sleep(3)
                            names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                            if names==[] :
                                    if disease_name_lang=="" :
                                        disease_name_lang= splitted_again.encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" ; "+splitted_again.encode("utf-8")
                                    if transliterated_name=="" :
                                        transliterated_name=splitted_again.encode("utf-8")
                                    else :
                                        transliterated_name=transliterated_name+" ; "+splitted_again.encode("utf-8")
                            else :
                                transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                                if transliterated_name=="" :
                                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                                else :
                                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                                for index in range(len(names)) :
                                    if index==0 :
                                        if disease_name_lang=="":
                                            disease_name_lang= names[index].encode("utf-8")
                                        else :
                                            disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    else :
                        if disease_name_lang=="" :
                            disease_name_lang= splitted.encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" ; "+splitted.encode("utf-8")
                        if transliterated_name=="" :
                            transliterated_name=splitted.encode("utf-8")
                        else :
                            transliterated_name=transliterated_name+" ; "+splitted.encode("utf-8")
                else :
                    transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                    if transliterated_name=="" :
                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                    else :
                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                    for index in range(len(names)) :
                        if index==0 :
                            if disease_name_lang=="":
                                disease_name_lang= names[index].encode("utf-8")
                            else :
                                disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    print disease_name_lang
        else :
         disease_name_lang=disease.encode("utf-8")
         transliterated_name=disease.encode("utf-8")
    else :
        transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
        transliterated_name=transliterate[0].encode("utf-8")[1:]
        for index in range(len(names)) :
            if index==0 :
                disease_name_lang= names[index].encode("utf-8")
            else :
                disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
        print disease_name_lang
    print "final disease name :",disease_name_lang
    print "transliterate :",transliterated_name
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Hindi_Disease_Shabdkosh =\""+ disease_name_lang.decode("utf-8") +"\" , Hindi_Transliterate_Shabdkosh =\""+ transliterated_name.decode("utf-8") +"\"  WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    #print update_query
    time.sleep(3)
   


#############################################   punjabi translate  shabdkosh ################################  

for disease in disease_name :
    print "disease :",disease
    main_page=requests.get('http://www.shabdkosh.com/pa/translate?e='+disease+'&l=pa')
    main_tree = html.fromstring(main_page.text)
    transliterated_name=""
    names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
    disease_name_lang=""
    if names==[] :
        disease_split=re.split("/|\|,| ",disease)
        if len(disease_split)>1:
            for splitted in disease_split:
                print splitted
                time.sleep(10)
                main_page=requests.get('http://www.shabdkosh.com/pa/translate?e='+splitted+'&l=pa')
                main_tree = html.fromstring(main_page.text)
                
                names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                if names==[] :
                    if "-" in splitted :
                        disease_split_again=re.split("-",splitted)
                        for splitted_again in disease_split_again:
                            print splitted_again
                            main_page=requests.get('http://www.shabdkosh.com/pa/translate?e='+splitted_again+'&l=pa')
                            main_tree = html.fromstring(main_page.text)
                            time.sleep(10)
                            names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                            if names==[] :
                                    if disease_name_lang=="" :
                                        disease_name_lang= splitted_again.encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" ; "+splitted_again.encode("utf-8")
                                    if transliterated_name=="" :
                                        transliterated_name=splitted_again.encode("utf-8")
                                    else :
                                        transliterated_name=transliterated_name+" ; "+splitted_again.encode("utf-8")
                            else :
                                transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                                if transliterated_name=="" :
                                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                                else :
                                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                                for index in range(len(names)) :
                                    if index==0 :
                                        if disease_name_lang=="":
                                            disease_name_lang= names[index].encode("utf-8")
                                        else :
                                            disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    else :
                        if disease_name_lang=="" :
                            disease_name_lang= splitted.encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" ; "+splitted.encode("utf-8")
                        if transliterated_name=="" :
                            transliterated_name=splitted.encode("utf-8")
                        else :
                            transliterated_name=transliterated_name+" ; "+splitted.encode("utf-8")
                else :
                    transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                    if transliterated_name=="" :
                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                    else :
                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                    for index in range(len(names)) :
                        if index==0 :
                            if disease_name_lang=="":
                                disease_name_lang= names[index].encode("utf-8")
                            else :
                                disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    print disease_name_lang
        else :
         disease_name_lang=disease.encode("utf-8")
         transliterated_name=disease.encode("utf-8")
    else :
        transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
        transliterated_name=transliterate[0].encode("utf-8")[1:]
        for index in range(len(names)) :
            if index==0 :
                disease_name_lang= names[index].encode("utf-8")
            else :
                disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
        print disease_name_lang
    print "final disease name :",disease_name_lang
    print "transliterate :",transliterated_name
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Punjabi_Disease_Shabdkosh =\""+ disease_name_lang.decode("utf-8") +"\" , Punjabi_Transliterate_Shabdkosh =\""+ transliterated_name.decode("utf-8") +"\"  WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    #print update_query
    time.sleep(10)
    
 
#############################################   gujarati translate  shabdkosh ################################     
    
for disease in disease_name :
    print "disease :",disease
    main_page=requests.get('http://www.shabdkosh.com/gu/translate?e='+disease+'&l=gu')
    main_tree = html.fromstring(main_page.text)
    transliterated_name=""
    names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
    disease_name_lang=""
    if names==[] :
        disease_split=re.split("/|\|,| ",disease)
        if len(disease_split)>1:
            for splitted in disease_split:
                print splitted
                time.sleep(10)
                main_page=requests.get('http://www.shabdkosh.com/gu/translate?e='+splitted+'&l=gu')
                main_tree = html.fromstring(main_page.text)
                
                names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                if names==[] :
                    if "-" in splitted :
                        disease_split_again=re.split("-",splitted)
                        for splitted_again in disease_split_again:
                            print splitted_again
                            main_page=requests.get('http://www.shabdkosh.com/gu/translate?e='+splitted_again+'&l=gu')
                            main_tree = html.fromstring(main_page.text)
                            time.sleep(10)
                            names=main_tree.xpath("///*[@id=\"left\"]/div[2]/div/ol/li/a/text()")
                            if names==[] :
                                    if disease_name_lang=="" :
                                        disease_name_lang= splitted_again.encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" ; "+splitted_again.encode("utf-8")
                                    if transliterated_name=="" :
                                        transliterated_name=splitted_again.encode("utf-8")
                                    else :
                                        transliterated_name=transliterated_name+" ; "+splitted_again.encode("utf-8")
                            else :
                                transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                                if transliterated_name=="" :
                                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                                else :
                                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                                for index in range(len(names)) :
                                    if index==0 :
                                        if disease_name_lang=="":
                                            disease_name_lang= names[index].encode("utf-8")
                                        else :
                                            disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                                    else :
                                        disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    else :
                        if disease_name_lang=="" :
                            disease_name_lang= splitted.encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" ; "+splitted.encode("utf-8")
                        if transliterated_name=="" :
                            transliterated_name=splitted.encode("utf-8")
                        else :
                            transliterated_name=transliterated_name+" ; "+splitted.encode("utf-8")
                else :
                    transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
                    if transliterated_name=="" :
                        transliterated_name=transliterate[0].encode("utf-8")[1:]
                    else :
                        transliterated_name=transliterated_name+" ; "+transliterate[0].encode("utf-8")[1:]
                    for index in range(len(names)) :
                        if index==0 :
                            if disease_name_lang=="":
                                disease_name_lang= names[index].encode("utf-8")
                            else :
                                disease_name_lang= disease_name_lang+" ; " + names[index].encode("utf-8")
                        else :
                            disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
                    print disease_name_lang
        else :
         disease_name_lang=disease.encode("utf-8")
         transliterated_name=disease.encode("utf-8")
    else :
        transliterate=main_tree.xpath("//*[@id=\"left\"]/text()")
        transliterated_name=transliterate[0].encode("utf-8")[1:]
        for index in range(len(names)) :
            if index==0 :
                disease_name_lang= names[index].encode("utf-8")
            else :
                disease_name_lang= disease_name_lang+" , "+names[index].encode("utf-8")
        print disease_name_lang
    print "final disease name :",disease_name_lang
    print "transliterate :",transliterated_name
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Gujarati_Disease_Shabdkosh =\""+ disease_name_lang.decode("utf-8") +"\" , Gujarati_Transliterate_Shabdkosh =\""+ transliterated_name.decode("utf-8") +"\"  WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    #print update_query
    time.sleep(10)
"""
#############################################   hindi translate hindkhoj ################################    

def isEnglish(s):
    try:
        s.decode('ascii')
    except :
        return False
    else:
        return True
        
#ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
for disease in disease_name :
    print "disease :",disease
    main_page=requests.get('http://dict.hinkhoj.com/hindi-dictionary.php?word='+disease)
    main_tree = html.fromstring(main_page.text)
    list_names=""
    type_names=""
    list_names_final=""
    type_names_final=""
    names_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/span/text()")
    found=False
    count=0
    index=0
    while index < len(names_hinkhoj) :
        if names_hinkhoj[index].lower()==disease.replace("-"," ").replace("/"," ").replace(".","") :
            index+=1
            if index < len(names_hinkhoj) :
                if list_names=="" :
                    list_names=names_hinkhoj[index].encode("utf-8").replace("\n","")
                else :
                    list_names=list_names+" , "+names_hinkhoj[index].encode("utf-8").replace("\n","")
                count+=1
                found=True
            index+=1
        
        else :
            break
        
    if found==True :
        type_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/text()")
        count_type=0
        for index2 in range(len(type_hinkhoj)) :
            name=type_hinkhoj[index2]
            if name.lower() in ["noun","verb","adjective","adverb"]:
                  if count_type < count :
                    count_type+=1
                    if type_names=="" :
                        type_names=name.lower()
                    else:
                        type_names=type_names+" , "+ name.lower()
                  else :
                     break
        list_names_final=list_names
        type_names_final=type_names
    
    #print list_names
    #print type_names
    
    
    else :
        disease_split=re.split("/|\|,| ",disease)
        if len(disease_split)>1:
            for splitted in disease_split:
                    print splitted
                    time.sleep(10)
                    main_page=requests.get('http://dict.hinkhoj.com/hindi-dictionary.php?word='+splitted)
                    main_tree = html.fromstring(main_page.text)
                    list_names=""
                    type_names=""
                    names_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/span/text()")
                    found=False
                    count=0
                    index=0
                    while index < len(names_hinkhoj) :
                        if names_hinkhoj[index].lower()==splitted.replace("-"," ").replace("/"," ").replace(".","") :
                            index+=1
                            if index < len(names_hinkhoj) :
                                if list_names=="" :
                                    list_names=names_hinkhoj[index].encode("utf-8").replace("\n","")
                                else :
                                    list_names=list_names+" , "+names_hinkhoj[index].encode("utf-8").replace("\n","")
                                count+=1
                                found=True
                            index+=1
                        
                        else :
                            break
                        
                    if found==True :
                        type_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/text()")
                        count_type=0
                        for index in range(len(type_hinkhoj)) :
                            name=type_hinkhoj[index]
                            if name.lower() in ["noun","verb","adjective","adverb"]:
                                  if count_type < count :
                                    count_type+=1
                                    if type_names=="" :
                                        type_names=name.lower()
                                    else:
                                        type_names=type_names+" , "+ name.lower()
                                  else :
                                     break
                        
                        if list_names_final=="" :
                            list_names_final=list_names
                            type_names_final=type_names
                        else :
                            list_names_final=list_names_final+" ; "+list_names
                            type_names_final=type_names_final+" ; "+type_names
                    
                    else :
                         if "-" in splitted :
                            disease_split_again=re.split("-",splitted)
                            for splitted_again in disease_split_again:
                                print splitted_again
                                time.sleep(10)
                                main_page=requests.get('http://dict.hinkhoj.com/hindi-dictionary.php?word='+splitted_again)
                                main_tree = html.fromstring(main_page.text)
                                list_names=""
                                type_names=""
                                names_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a/span/text()")
                                found=False
                                count=0
                                index=0
                                while index < len(names_hinkhoj) :
                                    if names_hinkhoj[index].lower()==splitted_again.replace("-"," ").replace("/"," ").replace(".","") :
                                        index+=1
                                        if index < len(names_hinkhoj) :
                                            count+=1
                                            found=True
                                            if list_names=="" :
                                                list_names=names_hinkhoj[index].encode("utf-8").replace("\n","")
                                            else :
                                                list_names=list_names+" , "+names_hinkhoj[index].encode("utf-8").replace("\n","")
                                        index+=1
                                    
                                    else :
                                        break
                                    
                                if found==True :
                                    type_hinkhoj=main_tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/text()")
                                    count_type=0
                                    for index in range(len(type_hinkhoj)) :
                                        name=type_hinkhoj[index]
                                        if name.lower() in ["noun","verb","adjective","adverb"]:
                                              if count_type < count :
                                                count_type+=1
                                                if type_names=="" :
                                                    type_names=name.lower()
                                                else:
                                                    type_names=type_names+" , "+ name.lower()
                                              else :
                                                 break
                                    
                                    if list_names_final=="" :
                                        list_names_final=list_names
                                        type_names_final=type_names
                                    else :
                                        list_names_final=list_names_final+" ; "+list_names
                                        type_names_final=type_names_final+" ; "+type_names
                                else :
                                    if list_names_final=="" :
                                        list_names_final=splitted_again.encode("utf-8")
                                        type_names_final="none"
                                    else :
                                        list_names_final=list_names_final+" ; "+splitted_again.encode("utf-8")
                                        type_names_final=type_names_final+" ; "+"none"
                            
                         else :
                            if list_names_final=="" :
                                list_names_final=splitted.encode("utf-8")
                                type_names_final="none"
                            else :
                                list_names_final=list_names_final+" ; "+splitted.encode("utf-8")
                                type_names_final=type_names_final+" ; "+"none"
        else :
            if list_names_final=="" :
                list_names_final=disease.encode("utf-8")
                type_names_final="none"
            else :
                list_names_final=list_names_final+" ; "+disease.encode("utf-8")
                type_names_final=type_names_final+" ; "+"none"
                
                
    print list_names_final
    print type_names_final
    update_query="UPDATE `Disease_names`.`Disease_Ontology_Multi` SET Hindi_Disease_Hinkhoj =\""+ list_names_final.decode("utf-8") +"\" , Hindi_Type_Hinkhoj =\""+ type_names_final +"\"  WHERE English_Disease = \""+ disease +"\""
    try:
       cursor.execute(update_query)
       db.commit()
    except Exception, e: 
        print update_query
        print str(e)
        db.rollback()
    #print update_query
    time.sleep(10)
            
