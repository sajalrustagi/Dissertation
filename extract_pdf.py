# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:40:25 2015

@author: sajal
"""

from lxml import html
import os.path
import requests
import PyPDF2
import re
from roman import toRoman,romanNumeralPattern
import MySQLdb
from time import ctime
pdf_urls=[]
import unicodedata

db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()

def extract_file(filename) :
    global dict_page 
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    count =1
    extra_count=1
    state="" 
    new_remove_count=1
    text_split=[]
    text=""
    last_stored=0
    dict_page={}
    dict_page['filename']= []
    dict_page['city']= []
    dict_page['disease']= []
    dict_page['case'] = []
    dict_page['death']= []
    dict_page['start date']= []
    dict_page['reporting date']= []
    dict_page['status']=[]
    dict_page['roman']=[]
    roman=""
    last_one=0
    end_text=""
    last_text_split=[]
    last_roman=""
    for pages in range(pdfReader.numPages):
       #print "page no.",pages
       if pages!=0:
        
        
        maxi_=0
        
        pageObj = pdfReader.getPage(pages)
        last_text=text
        text= pageObj.extractText()
        
        old_text_split=text_split
        text_split=re.split('outbreak|case|given|a total',text.lower())
        ultimate_done=False
        #print text_split
        #raw_input("Press ENTER to exit")
        disease=""
        Cases=""
        Death=""
        Start_Date=""
        Reporting_Date=""
        Status=""
        city=""
        for item in range(len(text_split)) :
            maxi_=len(old_text_split)-1
            try :
              #print text_split[item]
              extra_roman= " "+str(toRoman(new_remove_count))+"."
              str_roman= " "+str(toRoman(count))+"."
              if count!=1:
                  prev_str_roman= " "+str(toRoman(count-1))+"."
              else :
                  prev_str_roman=str_roman
              next_str_roman= " "+str(toRoman(count+1))+"."
              #print "roman ",str(toRoman(count))
              if text_split[item].replace("\n","").find(str_roman)==-1 and text_split[item].replace("\n","").find(prev_str_roman)==-1 and text_split[item].replace("\n","").find(next_str_roman)==-1:
                  str_roman= " "+str(toRoman(count))+" "
                  if count!=1:
                      prev_str_roman= " "+str(toRoman(count-1))+" "
                  else :
                      prev_str_roman=str_roman
                  next_str_roman= " "+str(toRoman(count+1))+" "
              if text_split[item].replace("\n","").find(str_roman)==-1 and text_split[item].replace("\n","").find(prev_str_roman)==-1 and text_split[item].replace("\n","").find(next_str_roman)==-1:
                  if text_split[item].replace("\n","").replace(" ","")!="." and (text_split[item].replace("\n","").find("under control")>=0 or text_split[item].replace("\n","").find("under surveillance")>=0):
                    find_control=text_split[item].replace("\n","").find("under control")
                    if find_control ==-1:
                       find_control=text_split[item].replace("\n","").find("under surveillance")
                    while text_split[item].replace("\n","")[find_control-1] ==" " :
                        find_control-=1
                    if text_split[item].replace("\n","")[find_control-1].isdigit()==False :
                        continue
                    
                    #print text_split[item]
                    #raw_input("Press ENTER to exit")
                    
                    count+=1
                    roman_split=text_split[item]
              
    
                    roman_split_newline=roman_split.split("\n")
                    
                    #print roman_split_newline
                    new_count=-1
                    done=False
                    if text_split[item].replace("\n","").find(extra_roman)==-1:
                        extra_roman= " "+str(toRoman(new_remove_count))+" "
                    if text_split[item].replace("\n","").find(extra_roman)>=0:
                        ultimate_done=True
                        new_remove_count+=1
                    times_count=0
                    disease=""
                    Cases=""
                    Death=""
                    Start_Date=""
                    Reporting_Date=""
                    Status=""
                    city=""
                    no_date=False
                    while (done==False) :
                        #raw_input("Press ENTER to exit")
                        while roman_split_newline[new_count] == " " or roman_split_newline[new_count] == "" :
                            new_count-=1
                        if times_count==0:
                            while roman_split_newline[new_count][-1].isdigit() != True:
                                #print roman_split_newline[new_count][-1]
                                if roman_split_newline[new_count]!=" ":
                                    Status=roman_split_newline[new_count]+Status
                                new_count-=1
                            split_status=Status.split(" ")
                            if len(split_status)>2 :
                                    Status=split_status[0]+" "+split_status[1]
                            #print "\nin status ",Status
    #                        disease=disease.replace("?","")
                        elif times_count==1:
                            while  roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                Reporting_Date=roman_split_newline[new_count]+Reporting_Date
                                new_count-=1
                            #print "I date ",Reporting_Date
                        elif times_count==2:
                            if (roman_split_newline[new_count-1]=="" or roman_split_newline[new_count-1]==" ") and len(re.split('/|\.',roman_split_newline[new_count]))==1:
                                    Start_Date=Reporting_Date
                                    Reporting_Date=""
                                    Death=roman_split_newline[new_count]
                                    
                                    new_count-=1
                                    no_date=True
                                    #print "II date ",Start_Date
                                    #print "Death ",Death
                            else :
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    Start_Date=roman_split_newline[new_count]+Start_Date
                                    new_count-=1
                                #print "II date ",Start_Date 
                        elif times_count==3:
                            if no_date:
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    Cases=roman_split_newline[new_count]
                                    new_count-=1
                                #print "Case ",Cases
                            else :
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    Death=roman_split_newline[new_count]
                                    new_count-=1
                                #print "Death ",Death
                            
                        elif times_count==4:
                            if no_date:
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    disease=roman_split_newline[new_count]+disease
                                    new_count-=1
                                disease=disease.replace("?","")
                                #print "Disease ",disease
                            else :
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    Cases=roman_split_newline[new_count]
                                    new_count-=1
                                #print "Case ",Cases
                            
                        elif times_count==5:
                            if no_date:
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    city=roman_split_newline[new_count]+city
                                    new_count-=1
                                done=True
                                #print "City ",city
                            else :
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    disease=roman_split_newline[new_count]+disease
                                    new_count-=1
                                disease=disease.replace("?","")
                                #print "Disease ",disease
                        elif times_count==6:
                            while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "":
                                    city=roman_split_newline[new_count]+city
                                    new_count-=1
                            #print "City ",city
                            done=True
                        times_count+=1
                        
                   
                    #raw_input("Press ENTER to exit")
                    #print city, disease,Cases, Death, Start_Date , Reporting_Date,Status,str_roman
                    Cases=Cases.replace("#","")
                    Death=Death.replace("#","")
                    if city[0]=="(" and city[-1]==")" :
                        city=city[1:-1]
                    dict_page['filename']=dict_page['filename']+[filename.split("/")[-1].split(".")[0]]
                    dict_page['city']=dict_page['city']+[city]
                    dict_page['disease']= dict_page['disease']+[disease]
                    dict_page['case']=dict_page['case']+[Cases]
                    dict_page['death']= dict_page['death']+[Death]
                    dict_page['start date']= dict_page['start date']+[Start_Date] 
                    dict_page['reporting date']= dict_page['reporting date']+[Reporting_Date]
                    dict_page['status']=dict_page['status']+[Status]
                    dict_page['roman']=dict_page['roman']+[str_roman]
                    if city==""  or Cases=="" or Start_Date=="" or ultimate_done==True or Status=="" or disease=="" or Death=="":
                        print 
                    else :
                        if ((not romanNumeralPattern.search(city.replace(".","")) )==False) or  len(re.split("/|\.|-",Start_Date)) !=3 or city.replace(".","").isdigit()==True  or (Reporting_Date!="" and len(re.split("/|\.|-",Reporting_Date)) !=3) or Death.isdigit()==False or Cases.isdigit()==False:
                                print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                                #raw_input("Press ENTER to exit")
                        else :
                            
#                                print "last :", last_stored
#                            print last_stored+1
#                            print item
                            if last_stored >item :
#                                    print "here changed :",old_text_split[last_stored+1:maxi_]
#                                    print old_text_split[last_stored+1].replace("\n","")
#                                    print old_text_split[maxi_].replace("\n","")
#                                    print last_text.lower().replace("\n","")
                                    index_start=last_text.lower().replace("\n","").find(old_text_split[last_stored+1].replace("\n","")) -6
#                                    print "start ", index_start
                                    len_add=0
                                    if last_text.lower().replace("\n","").count(old_text_split[maxi_].replace("\n",""))> 1:
                                        len_add=len_add+ len(old_text_split[maxi_].replace("\n",""))           
                                        index_max=maxi_-1
                                        len_add=len_add+ len(old_text_split[index_max].replace("\n","")) 
                                        while last_text.lower().replace("\n","").count(old_text_split[index_max].replace("\n",""))> 1:
                                               
                                           index_max=index_max-1
                                           len_add=len_add+ len(old_text_split[index_max].replace("\n",""))
#                                           print "index_max :",index_max
                                    else :
                                        index_max=maxi_
                                        len_add=len_add+ len(old_text_split[index_max].replace("\n",""))  
                                    index_end=last_text.lower().replace("\n","").find(old_text_split[index_max].replace("\n",""))+len_add
#                                    print "end ", index_end
                                    final_text_output= last_text.replace("\n","")[index_start:index_end]
                                    last_stored=0
                            else :
                                
#                                print "not changed :",text_split[last_stored+1:item]
#                                print text_split[last_stored+1]
#                                print text.replace("\n","")
                                index_start=text.lower().replace("\n","").find(text_split[last_stored+1].replace("\n","")) -6
                                if last_stored+1==item :
                                    index_end=text.lower().replace("\n","").find(text_split[item+1].replace("\n",""))
                                else :
                                    index_end=text.lower().replace("\n","").find(text_split[item].replace("\n",""))
                                
                                    
                                final_text_output= text.replace("\n","")[index_start:index_end+1]
                            if final_text_output[1]==" " :
                                    final_text_output= final_text_output[2:]
                            elif (final_text_output[0]=="t" and final_text_output[1]=="b"):
                                    final_text_output= "Ou"+final_text_output
                            if roman in dict_page['roman'] :
                                    index_roman=dict_page['roman'].index(roman)
                                    final_text_output=final_text_output.encode('ascii','ignore')
                                    update_sql = "UPDATE Disease_incidents_India SET Report =\""+ final_text_output +"\"  WHERE City = \""+ dict_page['city'][index_roman] +"\" and Disease =\""+ dict_page['disease'][index_roman] +"\" and Filename = \""+ dict_page['filename'][index_roman]  +"\"and Cases = "+ str(int( dict_page['case'][index_roman])) +" and Death = "+ str(int( dict_page['death'][index_roman])) +" and Status =\""+ dict_page['status'][index_roman] +"\""
                                    
                                    try:
                                                   # Execute the SQL command
                                       cursor.execute(update_sql)
                                       #print update_sql
                                       # Commit your changes in the database
                                       print update_sql
                                       db.commit()
                                    except Exception, e: 
                                        print repr(e)
                                        #print insert_query
                                       # Rollback in case there is any error
                                        db.rollback()
#                                    for keys in dict_page:
#                                        print dict_page[keys][index_roman]
#                            print final_text_output
                            last_stored=item
                            last_one=item
                            end_text=text.replace("\n" , "")
                            last_text_split=text_split
                            last_roman=str_roman
#                                print "new :", item
                            roman=str_roman
#                            print "last :", last_stored
#                            last_stored=item
#                            print "new :", item
                            Cases=int(Cases)
                            Death=int(Death)
                            split_date=re.split("/|\.|-",Start_Date)
                            split_date_modified=split_date[0]+"/"+split_date[1]+"/"+split_date[2]
                            if len(split_date[2])==2:
                                if Reporting_Date=="":
                                    insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                else :
                                    split_report_date=re.split("/|\.|-",Reporting_Date)
                                    split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                    if len(split_report_date[2])==2:
                                      insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                    else :
                                      insert_query="INSERT INTO Disease_incidents_India  (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"                                           
                                #print insert_query
                            else :
                                if Reporting_Date=="":
                                    insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                else :
                                    split_report_date=re.split("/|\.|-",Reporting_Date)
                                    split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                    if len(split_report_date[2])==2:
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                    else :
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"                                    
                                #print insert_query
                            try:
                       # Execute the SQL command
                                   cursor.execute(insert_query)
                                   print insert_query
                                   # Commit your changes in the database
                                   db.commit()
                            except Exception, e: 
                                    print repr(e)
                                    #print insert_query
                                   # Rollback in case there is any error
                                    db.rollback()
                            #print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                        
              else :
                     
                    
                    text_split=re.split('outbreak|case|given',text.replace("\n","").lower())
                    if text_split[item].replace("\n","").replace(" ","")!="." and ((text_split[item].replace("\n","").find(str_roman)>=0 and str_roman not in dict_page['roman']) or (text_split[item].replace("\n","").find(prev_str_roman)>=0 and prev_str_roman not in dict_page['roman']) or (text_split[item].replace("\n","").find(next_str_roman)>=0 and next_str_roman not in dict_page['roman'])):
                        #print "text_split final :", text_split[item]
                        count+=1
                        #print "count increased to ",count
                        roman_split=re.split(str_roman+"|"+prev_str_roman+"|"+next_str_roman,text_split[item])
        
                        
                        new_count=-1
                        roman_split_newline=roman_split[0]
                        while roman_split_newline[new_count] == " " or roman_split_newline[new_count] == "\n" or roman_split_newline[new_count] == "":
                            new_count-=1
                        old_city=city
                        city=""
                        try :
                            while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "\n" and roman_split_newline[new_count] != "" and roman_split_newline[new_count] != ".":
                                    city=roman_split_newline[new_count]+city
                                    new_count-=1
                        except :
                            print "no city name"
                        if city=="" or city == "taken" or city == "done":
                            city=old_city
                        new_split=re.split('outbreak|case|given',roman_split[1].lower())[0]
                        #print "here new_spli_line :",new_split
                        new_count=0
                        done=False
                        roman_split_newline=new_split
                        times_count=0
                        disease=""
                        Cases=""
                        Death=""
                        Start_Date=""
                        Reporting_Date=""
                        Status=""
                        #raw_input("Press ENTER to exit")
                        while (done==False) :
                            
                            while roman_split_newline[new_count] == " " or roman_split_newline[new_count] == "\n" or roman_split_newline[new_count] == "/":
                                new_count+=1
                            if times_count==0:
                                while roman_split_newline[new_count].isdigit()==False:
                                    disease=disease+roman_split_newline[new_count]
                                    new_count+=1
                                disease=disease.replace("?","")
                            elif times_count==1:
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "/" and roman_split_newline[new_count].isdigit()!=False :
                                    Cases=Cases+roman_split_newline[new_count]
                                    new_count+=1
                                if  roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "/" and roman_split_newline[new_count].isdigit()==False :
                                    done=True
#                                    if len(roman_split_newline)<50:
#                                        count-=1
                                    break
                            elif times_count==2:
                                while roman_split_newline[new_count] != " " and roman_split_newline[new_count].isdigit()!=False:
                                    Death=Death+roman_split_newline[new_count]
                                    new_count+=1
                                if  roman_split_newline[new_count] != " "  and roman_split_newline[new_count].isdigit()==False :
#                                    if len(roman_split_newline)<50:
#                                        count-=1                                    
                                    done=True
                                    
                                    break
                            elif times_count==3:
                                while roman_split_newline[new_count] != " " :
                                    Start_Date=Start_Date+roman_split_newline[new_count]
                                    new_count+=1
                            elif times_count==4:
                                #print "here :",roman_split_newline[new_count]
                                if roman_split_newline[new_count].find("u")>=0 :
                                    while new_count != len(roman_split_newline)-1:
                                        Status=Status+roman_split_newline[new_count]
                                        new_count+=1
                                    Status=Status+roman_split_newline[new_count]
                                    done=True
                                    split_status=Status.split(" ")
                                    if len(split_status)>2 :
                                        Status=split_status[0]+" "+split_status[1]
                                        
                                else :
                                    while roman_split_newline[new_count] != " " :
                                        Reporting_Date=Reporting_Date+roman_split_newline[new_count]
                                        new_count+=1
                            elif times_count==5:
                                while new_count != len(roman_split_newline)-1 :
                                        Status=Status+roman_split_newline[new_count]
                                        new_count+=1
                                Status=Status+roman_split_newline[new_count]
                                done=True
                                split_status=Status.split(" ")
                                if len(split_status)>2 :
                                        Status=split_status[0]+" "+split_status[1]
                            times_count+=1
                        Cases=Cases.replace("#","")
                        Death=Death.replace("#","")
                        if city[0]=="(" and city[-1]==")" :
                            city=city[1:-1]
                        #print "roman here",str_roman
                        dict_page['filename']=dict_page['filename']+[filename.split("/")[-1].split(".")[0]]
                        dict_page['city']=dict_page['city']+[city]
                        dict_page['disease']= dict_page['disease']+[disease]
                        dict_page['case']=dict_page['case']+[Cases]
                        dict_page['death']= dict_page['death']+[Death]
                        dict_page['start date']= dict_page['start date']+[Start_Date] 
                        dict_page['reporting date']= dict_page['reporting date']+[Reporting_Date]
                        dict_page['status']=dict_page['status']+[Status]
                        dict_page['roman']=dict_page['roman']+[str_roman]
                        if city==""  or Cases=="" or Start_Date=="" or Status=="" or disease=="" or Death=="":
                            print 
                        else :
                            
#                                
#                            
#                            city=city.replace(".","") 
                            if ((not romanNumeralPattern.search(city.replace(".","")) )==False) or  len(re.split("/|\.|-",Start_Date)) !=3 or city.replace(".","").isdigit()==True  or (Reporting_Date!="" and len(re.split("/|\.|-",Reporting_Date)) !=3) or Death.isdigit()==False or Cases.isdigit()==False:
                                print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                                #raw_input("Press ENTER to exit")
                            else :
                                
#                                print "last :", last_stored
                                if last_stored >item :
#                                    print "here changed :",old_text_split[last_stored+1:maxi_]
#                                    print old_text_split[last_stored+1]
#                                    print old_text_split[maxi_]
#                                    print last_text.lower().replace("\n","")
                                    len_add=0
                                    index_start=last_text.lower().replace("\n","").find(old_text_split[last_stored+1]) -6
#                                    print "start ", index_start
                                    if last_text.lower().replace("\n","").count(old_text_split[maxi_])>1:
                                        #print "here"         
                                        len_add=len_add+ len(old_text_split[maxi_])
                                        index_max=maxi_-1
                                        len_add=len_add+ len(old_text_split[index_max])
                                        while last_text.lower().replace("\n","").count(old_text_split[index_max])>1:  
                                           index_max=index_max-1                                           
                                           len_add=len_add+ len(old_text_split[index_max])  
                                    
#                                    if old_text_split[maxi_].replace(" ","")=="." :
#                                        index_max=maxi_-1
                                    else :
                                        index_max=maxi_
                                        len_add=len_add+ len(old_text_split[index_max])    
                                    index_end=last_text.lower().replace("\n","").find(old_text_split[index_max])+len_add
#                                    print "end ", index_end
                                    final_text_output= last_text.replace("\n","")[index_start:index_end]
                                else :
#                                    print "not changed :",text_split[last_stored+1:item]
                                    #print text_split[last_stored+1]
                                    #print text.replace("\n","")
                                    index_start=text.lower().replace("\n","").find(text_split[last_stored+1]) -6
                                    
                                    index_start=text.lower().replace("\n","").find(text_split[last_stored+1].replace("\n","")) -6
                                    if last_stored+1==item :
                                        index_end=text.lower().replace("\n","").find(text_split[item+1].replace("\n",""))
                                    else :
                                        index_end=text.lower().replace("\n","").find(text_split[item].replace("\n",""))
                                    final_text_output= text.replace("\n","")[index_start:index_end+1]
                                #print final_text_output
                                if final_text_output[1]==" " :
                                    final_text_output= final_text_output[2:]
                                elif (final_text_output[0]=="t" and final_text_output[1]=="b"):
                                    final_text_output= "Ou"+final_text_output
                                if roman in dict_page['roman'] :
                                    index_roman=dict_page['roman'].index(roman)
                                    final_text_output=final_text_output.encode('ascii','ignore')
                                    update_sql = "UPDATE Disease_incidents_India SET Report =\""+ final_text_output +"\"  WHERE City = \""+ dict_page['city'][index_roman] +"\" and Disease =\""+ dict_page['disease'][index_roman] +"\" and Filename = \""+ dict_page['filename'][index_roman]  +"\"and Cases = "+ str(int( dict_page['case'][index_roman])) +" and Death = "+ str(int( dict_page['death'][index_roman])) +" and Status =\""+ dict_page['status'][index_roman] +"\""
                                    
                                    try:
                                                   # Execute the SQL command
                                       cursor.execute(update_sql)
                                       print update_sql
                                       #print update_sql
                                       # Commit your changes in the database
                                       db.commit()
                                    except Exception, e: 
                                        print repr(e)
                                        #print insert_query
                                       # Rollback in case there is any error
                                        db.rollback()
#                                    for keys in dict_page:
#                                        print dict_page[keys][index_roman]
#                                print final_text_output
                                last_stored=item
#                                print "new :", item
                                roman=str_roman
                                last_one=item
                                end_text=text.replace("\n" , "")
                                last_text_split=text_split
                                last_roman=str_roman
                                Cases=int(Cases)
                                Death=int(Death)
                                split_date=re.split("/|\.|-",Start_Date)
                                split_date_modified=split_date[0]+"/"+split_date[1]+"/"+split_date[2]
                                if len(split_date[2])==2:
                                    if Reporting_Date=="":
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                    else :
                                        split_report_date=re.split("/|\.|-",Reporting_Date)
                                        split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                        if len(split_report_date[2])==2:
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                        else :
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"                                           
                                    #print insert_query
                                else :
                                    if Reporting_Date=="":
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                    else :
                                        split_report_date=re.split("/|\.|-",Reporting_Date)
                                        split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                        if len(split_report_date[2])==2:
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"
                                        else :
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[-1].split(".")[0])+"\");"                                    
                                    #print insert_query
                                try:
                       # Execute the SQL command
                                   cursor.execute(insert_query)
                                   print insert_query
                                   # Commit your changes in the database
                                   db.commit()
                                except Exception, e: 
                                    print repr(e)
                                    #print insert_query
                                   # Rollback in case there is any error
                                    db.rollback()
                            #print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                        
                        #print city, disease,Cases, Death, Start_Date , Reporting_Date,Status,str_roman

                        #raw_input("This is important")
              #print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
            except Exception,e :
                    pass
                    print e
                    #raw_input("Press ENTER to exit")
    #print "last_roman :", last_roman
#    if last_roman in dict_page['roman'] :
#        index_roman=dict_page['roman'].index(last_roman)
#        for keys in dict_page:
#            print dict_page[keys][index_roman]
#                                print "last :", last_stored

#                                    print "here changed :",old_text_split[last_stored+1:maxi_]
#                                    print old_text_split[last_stored+1]
#                                    print old_text_split[maxi_]
#                                    print last_text.lower().replace("\n","")
#    print end_text
#    print last_text_split[last_one+1:maxi_]
    try :
        index_start=end_text.lower().find(last_text_split[last_one+1].replace("\n","")) -6
    #    print "start ", index_start
    #    print last_text_split[last_one+1]
        maxi_=len(last_text_split)-1
    #                                    print "start ", index_start
    #    print "length",len(last_text_split[maxi_].replace(" ",""))
        len_add=0
        if end_text.lower().count(last_text_split[maxi_].replace("\n",""))>1:
            len_add=len_add+ len(last_text_split[maxi_].replace("\n",""))        
            index_max=maxi_-1
            len_add=len_add+ len(last_text_split[index_max].replace("\n",""))  
            while end_text.lower().count(last_text_split[index_max].replace("\n",""))>1:
                  
               index_max=index_max-1
               len_add=len_add+ len(last_text_split[index_max].replace("\n","")) 
        else :
            index_max=maxi_
            len_add=len_add+ len(last_text_split[index_max].replace("\n",""))  
    #    print last_text_split[index_max]
        index_end=end_text.lower().find(last_text_split[index_max].replace("\n",""))+len_add
    #    print "end ", index_end
    #                                    print "end ", index_end
        final_text_output= end_text.replace("\n","")[index_start:index_end]
        if final_text_output[1]==" " :
            final_text_output= final_text_output[2:]
        elif (final_text_output[0]=="t" and final_text_output[1]=="b"):
            final_text_output= "Ou"+final_text_output
        if last_roman in dict_page['roman'] :
            index_roman=dict_page['roman'].index(last_roman)
            final_text_output=final_text_output.encode('ascii','ignore')
            update_sql = "UPDATE Disease_incidents_India SET Report =\""+ final_text_output.replace("\"","'") +"\"  WHERE City = \""+ dict_page['city'][index_roman] +"\" and Disease =\""+ dict_page['disease'][index_roman] +"\" and Filename = \""+ dict_page['filename'][index_roman]  +"\"and Cases = "+ str(int( dict_page['case'][index_roman])) +" and Death = "+ str(int( dict_page['death'][index_roman])) +" and Status =\""+ dict_page['status'][index_roman] +"\""
            try:
                           # Execute the SQL command
               cursor.execute(update_sql)
               print update_sql

               #print update_sql
               # Commit your changes in the database
               db.commit()
            except Exception, e: 
                print repr(e)
                #print insert_query
               # Rollback in case there is any error
                db.rollback()
#            for keys in dict_page:
#                print dict_page[keys][index_roman]
#        print final_text_output
    except Exception , e:
        print str(e)
    

def extract_file_names () :
    global remove_url
    global pdf_urls
    global new_urls
    main_page=requests.get('http://www.idsp.nic.in/idsp/IDSP/outbreaks.htm')
    main_tree = html.fromstring(main_page.text)
    pdf_urls=main_tree.xpath("/html/body/table/tr/td/table/tr/td/a/@href")
    new_urls=[]
    #print pdf_urls
    for link in pdf_urls :
        out="/home/sajal/Desktop/Promed_scrap/PDFs/" + link.split("/")[-1]
        if os.path.isfile(out) :
            continue
        else :
            
            link="http://www.idsp.nic.in/idsp/IDSP/"+link
        
        r=requests.get(link)
        if str(r)=="<Response [404]>":
            remove_url=remove_url+[link.split("/")[-1]]
            continue
        new_urls=new_urls+[link.split("/")[-1]]
        print "begin :",out
        f=open(out,"w")
        f.write(r.content)
        f.close
        print "done :",out            

dict_page={}
print ctime()
remove_url=[]
new_urls=[]
found=False
extract_file_names()
for files in pdf_urls :
    #print files
    filename=files.split("/")[-1]
    if filename not in remove_url and filename in new_urls:
        extract_file("/home/sajal/Desktop/Promed_scrap/PDFs/"+filename)
    else :
        found=True

print 
    #if found==True :
    #raw_input("Press ENTER to exit")
    #print "\n" *100

#for files in os.listdir("PDFs/"):
#    print files
#    extract_file_14("PDFs/"+files.split("/")[-1])
#    raw_input("Press ENTER to exit")

#extract_file("PDFs/26th_wk12.pdf")
#        
