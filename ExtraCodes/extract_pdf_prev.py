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

db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()

def extract_file(filename) :
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    count =1
    extra_count=1
    state="" 
    new_remove_count=1
    for pages in range(pdfReader.numPages):
       #print "page no.",pages
       if pages!=0:
        pageObj = pdfReader.getPage(pages)
        text= pageObj.extractText()
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
                    if city==""  or Cases=="" or Start_Date=="" or ultimate_done==True or Status=="" or disease=="" or Death=="":
                        print 
                    else :
                        if ((not romanNumeralPattern.search(city.replace(".","")) )==False) or  len(re.split("/|\.|-",Start_Date)) !=3 or city.replace(".","").isdigit()==True  or (Reporting_Date!="" and len(re.split("/|\.|-",Reporting_Date)) !=3) or Death.isdigit()==False or Cases.isdigit()==False:
                                print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                                #raw_input("Press ENTER to exit")
                        else :
                            Cases=int(Cases)
                            Death=int(Death)
                            split_date=re.split("/|\.|-",Start_Date)
                            split_date_modified=split_date[0]+"/"+split_date[1]+"/"+split_date[2]
                            if len(split_date[2])==2:
                                if Reporting_Date=="":
                                    insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                else :
                                    split_report_date=re.split("/|\.|-",Reporting_Date)
                                    split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                    if len(split_report_date[2])==2:
                                      insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                    else :
                                      insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"                                           
                                #print insert_query
                            else :
                                if Reporting_Date=="":
                                    insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                else :
                                    split_report_date=re.split("/|\.|-",Reporting_Date)
                                    split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                    if len(split_report_date[2])==2:
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                    else :
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"                                    
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
                    if text_split[item].replace("\n","").replace(" ","")!="." and (text_split[item].replace("\n","").find(str_roman)>=0 or text_split[item].replace("\n","").find(prev_str_roman)>=0 or text_split[item].replace("\n","").find(next_str_roman)>=0):
                        count+=1
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
                        #print new_split
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
                        while (done==False) :
                            #raw_input("Press ENTER to exit")
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
                        if city==""  or Cases=="" or Start_Date=="" or Status=="" or disease=="" or Death=="":
                            print 
                        else :
#                            city=city.replace(".","") 
                            if ((not romanNumeralPattern.search(city.replace(".","")) )==False) or  len(re.split("/|\.|-",Start_Date)) !=3 or city.replace(".","").isdigit()==True  or (Reporting_Date!="" and len(re.split("/|\.|-",Reporting_Date)) !=3) or Death.isdigit()==False or Cases.isdigit()==False:
                                print "\nfilename :",filename.split("/")[1].split(".")[0],"\ncity :",city,"\ndisease :", disease,"\ncase :",Cases,"\ndeath :", Death,"\nstart date :", Start_Date ,"\nreporting date :", Reporting_Date,"\nstatus :",Status,"\nroman : ",str_roman,"\n"
                                #raw_input("Press ENTER to exit")
                            else :
                                Cases=int(Cases)
                                Death=int(Death)
                                split_date=re.split("/|\.|-",Start_Date)
                                split_date_modified=split_date[0]+"/"+split_date[1]+"/"+split_date[2]
                                if len(split_date[2])==2:
                                    if Reporting_Date=="":
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                    else :
                                        split_report_date=re.split("/|\.|-",Reporting_Date)
                                        split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                        if len(split_report_date[2])==2:
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                        else :
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"                                           
                                    #print insert_query
                                else :
                                    if Reporting_Date=="":
                                        insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),NULL,\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                    else :
                                        split_report_date=re.split("/|\.|-",Reporting_Date)
                                        split_report_date_modified=split_report_date[0]+"/"+split_report_date[1]+"/"+split_report_date[2]
                                        if len(split_report_date[2])==2:
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"
                                        else :
                                            insert_query="INSERT INTO Disease_incidents_India (  `City` ,  `Disease` ,  `Cases` ,  `Death` ,  `Start_Date` ,  `Reporting_Date` ,  `Status` ,  `Filename` ) VALUES( \""+str(city)+"\" , \""+str(disease)+"\" , "+str(Cases)+" ,"+str(Death)+" , STR_TO_DATE (\""+ str(split_date_modified) +"\", '%d/%m/%Y'),STR_TO_DATE (\""+ str(split_report_date_modified) +"\", '%d/%m/%Y'),\""+str(Status)+"\" ,\""+str(filename.split("/")[1].split(".")[0])+"\");"                                    
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
                    #print e
                    #raw_input("Press ENTER to exit")
                

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
