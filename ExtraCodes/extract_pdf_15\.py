# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:30:41 2015

@author: sajal
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:40:25 2015

@author: sajal
"""

from lxml import html
import os.path
import requests
import PyPDF2
from roman import toRoman
pdf_urls=[]

def extract_file(filename) :
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    count =1
    extra_count=1
    state="" 
    for pages in range(pdfReader.numPages):
       print "page no.",pages
       if pages!=0:
            pageObj = pdfReader.getPage(pages)
            text= pageObj.extractText()
            text_split=text.replace("\n","").lower().split("case")
            print 
            for item in range(len(text_split)) :
              str_roman= str(toRoman(count))+"."
              if text_split[item].replace("\n","").replace(" ","").find(str_roman)==-1:
                  str_roman= " "+str(toRoman(count))+" "
              if text_split[item].replace("\n","").replace(" ","")!="." and text_split[item].replace("\n","").find(str_roman)>=0:
                count+=1
                roman_split=text_split[item].split(str_roman)
                split_state=roman_split[0].split(str(extra_count) + ".")
                if len(split_state)==2 :
                    #print "here"
                    state="" 
                    extra_count+=1
                    #print split_state[1]
                    new_count_inside=0
                    roman_split_newline=split_state[1]
                    while roman_split_newline[new_count_inside] == " " or roman_split_newline[new_count_inside] == "\n" or roman_split_newline[new_count_inside] == "":
                        new_count_inside+=1
                       
                    while roman_split_newline[new_count_inside] != " " and roman_split_newline[new_count_inside] != "\n" and roman_split_newline[new_count_inside] != "":
                        state=state+roman_split_newline[new_count_inside]
                        new_count_inside+=1
                    #print state
                
                new_count=-1
                roman_split_newline=roman_split[0]
#                f=open("try.txt","a")
#                f.write(str(text_split[item]))
#                f.close
                while roman_split_newline[new_count] == " " or roman_split_newline[new_count] == "\n" or roman_split_newline[new_count] == "":
                    new_count-=1
                city=""
                while roman_split_newline[new_count] != " " and roman_split_newline[new_count] != "\n" and roman_split_newline[new_count] != "":
                        city=roman_split_newline[new_count]+city
                        new_count-=1
                #print "state",state
                
                new_split=roman_split[1].lower().split("case")[0]
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
                    while roman_split_newline[new_count] == " " or roman_split_newline[new_count] == "\n" or roman_split_newline[new_count] == "":
                        new_count+=1
                    if times_count==0:
                        while roman_split_newline[new_count].isdigit()==False:
                            disease=disease+roman_split_newline[new_count]
                            new_count+=1
                    elif times_count==1:
                        while roman_split_newline[new_count] != " " :
                            Cases=Cases+roman_split_newline[new_count]
                            new_count+=1
                    elif times_count==2:
                        while roman_split_newline[new_count] != " " :
                            Death=roman_split_newline[new_count]
                            new_count+=1
                    elif times_count==3:
                        while roman_split_newline[new_count] != " " :
                            Start_Date=Start_Date+roman_split_newline[new_count]
                            new_count+=1
                    elif times_count==4:
                        #print "here :",roman_split_newline[new_count]
                        if roman_split_newline[new_count].find("U")>=0 :
                            while new_count != len(roman_split_newline)-1:
                                Status=Status+roman_split_newline[new_count]
                                new_count+=1
                                done=True
#                            split_status=Status.split(" ")
#                            if len(split_status)>2 :
#                                if split_status[1]=="control" :
#                                    Status ="under control"
#                                else :
#                                    Status ="under surveillance"
                                
                        else :
                            while roman_split_newline[new_count] != " " :
                                Reporting_Date=Reporting_Date+roman_split_newline[new_count]
                                new_count+=1
                    elif times_count==5:
                        while new_count != len(roman_split_newline)-1 :
                                Status=Status+roman_split_newline[new_count]
                                new_count+=1
                        done=True
#                        split_status=Status.split(" ")
#                        if len(split_status)>2 :
#                                if split_status[1]=="control" :
#                                    Status ="under control"
#                                else :
#                                    Status ="under surveillance"
                    times_count+=1
                    
                #print "city :",city,"disease :", disease,"case :",Cases,"death :", Death,"start date :", Start_Date ,"reporting date :", Reporting_Date,"status :",Status
                print city, disease,Cases, Death, Start_Date , Reporting_Date,Status,str_roman

def extract_file_names () :
    print "here"
    global pdf_urls
    main_page=requests.get('http://www.idsp.nic.in/idsp/IDSP/outbreaks.htm')
    main_tree = html.fromstring(main_page.text)
    pdf_urls=main_tree.xpath("/html/body/table/tr/td/table/tr/td/a/@href")
    print pdf_urls
    for link in pdf_urls :
        out="PDFs/" + link.split("/")[-1]
        if os.path.isfile(out) :
            continue
        else :
            link="http://www.idsp.nic.in/idsp/IDSP/"+link
            print "begin :",out
            r=requests.get(link)
            f=open(out,"w")
            f.write(r.content)
            f.close
            print "done :",out
            
#extract_file_names()
#for files in pdf_urls :
#    print files
#    extract_file("PDFs/"+files.split("/")[-1])

for files in os.listdir("PDFs/"):
    print files
    extract_file("PDFs/"+files.split("/")[-1])

#extract_file("PDFs/13th_wk15.pdf")
#        
