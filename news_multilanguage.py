# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:05:10 2015

@author: sajal
"""
import requests
from lxml import html
from lxml import etree
import time,datetime

def isEnglish(s):
    try:
        for elem in s :
            elem.decode('ascii')
    except :
        return False
    else:
        return True

import MySQLdb
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()
"""
http://punjabi.jagran.com/news/national-news-punjabi.html
http://punjabi.jagran.com/news/national-news-punjabi-page2.html
http://punjabi.jagran.com/news/world-news-punjabi.html
http://punjabi.jagran.com/news/state-news-punjabi.html

//*[@id="1360140451380"]/div/div[3]/div[1]
//*[@id="content"]

http://jagbani.punjabkesari.in/national/
http://jagbani.punjabkesari.in/national//page/2

http://www.jagran.com/news/national-news-hindi.html
http://www.jagran.com/news/world-news-hindi.html

//*[@id="1378099854971"]/div[1]/ul/li[1]
//*[@id="1425987651970"]/section/section[2]/p[2]

http://www.amarujala.com/channels/samachar/national/

http://jagbani.punjabkesari.in/
http://jagbani.punjabkesari.in/international/page/23
http://jagbani.punjabkesari.in/national/page/23


http://www.punjabkesari.in/national/page/1000
http://www.punjabkesari.in/international

http://post.jagran.com/news-articles-world-news-1291790427-p5

"""
def execute_insert(insert_query) :
    try:
       cursor.execute(insert_query)
       db.commit()
    except Exception, e:
        print str(e)
        print insert_query
        db.rollback()
reqd_fmt = "%Y-%m-%d %H:%M:%S"

sql="SELECT distinct `URL` FROM `Articles_Multi_language`"
urls_done=[]
try :
    cursor.execute(sql)
    results = cursor.fetchall()
    for rows in results :
        urls_done=urls_done+[rows[0]]
except Exception,e :
        print "Not sql :",str(e)
"""
langs=["punjabi"]
#sources={'punjabi_sources':{"http://punjabi.jagran.com":["national","world","state"]}}
sources={'punjabi_sources':{"http://punjabi.jagran.com":["state"]}}

langs=["hindi"]
sources={'hindi_sources':{"http://www.jagran.com":["national","world"]}}

langs=["punjabi"]
sources={'punjabi_sources':{"http://jagbani.punjabkesari.in":["national","international"]}}
"""
langs=["hindi"]
sources={'hindi_sources':{"http://www.punjabkesari.in":["national","international"]}}
"""
langs=["english"]
sources={'english_sources':{"http://post.jagran.com":["india","world"]}}
"""
for lang in langs :
    sources_name=lang+"_sources"
    for source in sources[sources_name] :
        types=sources[sources_name][source]
        for type_ in types :
            count=0
            found=True
            if source == "http://post.jagran.com" :
                while found==True :
                    try :
                        count+=1
                        if type_=="india" :
                            numbers="1291789768"
                        else :
                            numbers="1291790427"
                        page_link=source+'/news-articles-'+type_+'-news-'+numbers+'-p'+str(count)
                        print
                        print page_link
                        print
                        main_page=requests.get(page_link)
                        time.sleep(5)
                        main_tree = html.fromstring(main_page.text)
                        link=main_tree.xpath("//*[@id=\"1408951307171\"]/div/div/div/div/h3/a/@href")
                        if len(link)==0:
                            found=False
                            continue
                        article_dates=main_tree.xpath("//*[@id=\"1408951307171\"]/div/div/div/div/div/p/text()")
                        article_texts=main_tree.xpath("//*[@id=\"1408951307171\"]/div/div/div/div/h3/a/text()")
                        for index in range(len(link)) :
                            article_url=link[index]
                            article_date=article_dates[index]
                            article_url=source+article_url
                            if article_url not in urls_done :
                                article_text=article_texts[index]
                                print article_url
                                main_page=requests.get(article_url)
                                time.sleep(5)
                                main_tree = html.fromstring(main_page.text)
                                #main_tree = etree.HTML(main_page.text)
                                articles=main_tree.xpath("//*[@id=\"1404295930615\"]/div/div/p/span/p/text()")
    #                            for article in articles:
    #                                content = etree.tostring(article)
    #                                print content
                                #article_date=article_date[0][12:-6]
                                d = datetime.datetime.strptime(article_date, '%d %b %Y, %I:%M %p')
                                article_date= datetime.date.strftime(d, reqd_fmt)
                                main_article=""
                                for article in articles:
                                    if article!="\n" and isEnglish(article.split()):
                                        main_article=main_article+article
                                main_article=main_article.replace("\"","'")
                                #print main_article
                                article_text=article_text.replace("\"","'")
                                if main_article!="" :
                                    insert_query="INSERT INTO  `Disease_names`.`Articles_Multi_language` (`Date` ,`Headline` ,`Article` ,`URL` ,`Source` ,`Language` ,`Category`)VALUES (\""+str(article_date)+"\",\""+article_text+"\",\""+  main_article+"\",\""+  article_url+"\",\""+  source+"\",\""+  str(lang)+"\",\""+  str(type_)+"\");"
                                    execute_insert(insert_query)
                                    #print insert_query
                    except Exception,e :
                        print str(e)
                        
                          
            elif source == "http://www.punjabkesari.in" :
                while found==True :
                    try :
                        count+=1
                        page_link=source+'/'+type_+'/page/'+str(count)
                        print
                        print page_link
                        print
                        main_page=requests.get(page_link)
                        time.sleep(5)
                        main_tree = html.fromstring(main_page.text)
                        link=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/h2/a/@href")
                        if len(link)==0:
                            found=False
                            continue
                        article_texts=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/h2/a/text()")
                        article_dates=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/div/div/text()")
                        for index in range(len(link)) :
                            article_url=link[index]
                            if article_url not in urls_done :
                                article_text=article_texts[index]
                                article_date=article_dates[index]
                                #article_url=source+article_url
                                print article_url
                                if not isEnglish(article_text.split()) :
                                    main_page=requests.get(article_url)
                                    time.sleep(5)
                                    main_tree = html.fromstring(main_page.text)
                                    articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dvStory\"]/p/span/text()")
                                    if len(articles)==0:
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dvStory\"]/p/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/div/div/div/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/p/span/span/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/div/text()")
                                    #article_date=article_date[0][12:-6]
                                    d = datetime.datetime.strptime(article_date, '%B %d, %Y %I:%M:%p')
                                    article_date= datetime.date.strftime(d, reqd_fmt)
                                    main_article=""
                                    for article in articles:
                                        if article!="\n" and not isEnglish(article.split()):
                                            main_article=main_article+article
                                    main_article=main_article.replace("\"","'")
                                    article_text=article_text.replace("\"","'")
                                    if main_article!="" :
                                        insert_query="INSERT INTO  `Disease_names`.`Articles_Multi_language` (`Date` ,`Headline` ,`Article` ,`URL` ,`Source` ,`Language` ,`Category`)VALUES (\""+str(article_date)+"\",\""+article_text+"\",\""+  main_article+"\",\""+  article_url+"\",\""+  source+"\",\""+  str(lang)+"\",\""+  str(type_)+"\");"
                                        execute_insert(insert_query)
                                #print insert_query
                    except Exception,e :
                        print str(e)
                        
            elif source == "http://jagbani.punjabkesari.in" :
                while found==True :
                    try :
                        count+=1
                        page_link=source+'/'+type_+'/page/'+str(count)
                        print
                        print page_link
                        print
                        main_page=requests.get(page_link)
                        time.sleep(5)
                        main_tree = html.fromstring(main_page.text)
                        link=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/h2/a/@href")
                        if len(link)==0:
                            found=False
                            continue
                        article_texts=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/h2/a/text()")
                        article_dates=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_secnws\"]/span/div/div/text()")
                        for index in range(len(link)) :
                            article_url=link[index]
                            if article_url not in urls_done :
                                article_text=article_texts[index]
                                article_date=article_dates[index]
                                #article_url=source+article_url
                                print article_url
                                if not isEnglish(article_text.split()) :
                                    main_page=requests.get(article_url)
                                    time.sleep(5)
                                    main_tree = html.fromstring(main_page.text)
                                    articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dvStory\"]/p/span/text()")
                                    if len(articles)==0:
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dvStory\"]/p/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/div/div/div/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/p/span/span/text()")
                                    if len(articles)==0: 
                                        articles=main_tree.xpath("//*[@id=\"ContentPlaceHolder1_dv_story\"]/div/text()")
                                    #article_date=article_date[0][12:-6]
                                    d = datetime.datetime.strptime(article_date, '%B %d, %Y %I:%M:%p')
                                    article_date= datetime.date.strftime(d, reqd_fmt)
                                    main_article=""
                                    for article in articles:
                                        if article!="\n" and not isEnglish(article.split()):
                                            main_article=main_article+article
                                    main_article=main_article.replace("\"","'")
                                    article_text=article_text.replace("\"","'")
                                    if main_article!="" :
                                        insert_query="INSERT INTO  `Disease_names`.`Articles_Multi_language` (`Date` ,`Headline` ,`Article` ,`URL` ,`Source` ,`Language` ,`Category`)VALUES (\""+str(article_date)+"\",\""+article_text+"\",\""+  main_article+"\",\""+  article_url+"\",\""+  source+"\",\""+  str(lang)+"\",\""+  str(type_)+"\");"
                                        execute_insert(insert_query)
                            #print insert_query
                    except Exception,e :
                        print str(e)
                        
            elif source == "http://punjabi.jagran.com" :
                while found==True :
                    try :
                        count+=1
                        page_link=source+'/news/'+type_+'-news-punjabi-page'+str(count)+'.html'
                        print
                        print page_link
                        print
                        main_page=requests.get(page_link)
                        time.sleep(5)
                        main_tree = html.fromstring(main_page.text)
                        link=main_tree.xpath("//*[@id=\"1360140451380\"]/div/div/div/h3/a/@href")
                        if len(link)==0:
                            found=False
                            continue
                        article_texts=main_tree.xpath("//*[@id=\"1360140451380\"]/div/div/div/h3/a/text()")
                        for index in range(len(link)) :
                            article_url=link[index]
                            article_url=source+article_url
                            if article_url not in urls_done :
                                article_text=article_texts[index]
                                print article_url
                                main_page=requests.get(article_url)
                                time.sleep(5)
                                main_tree = html.fromstring(main_page.text)
                                articles=main_tree.xpath("//*[@id=\"content\"]/p/text()")
                                article_date=main_tree.xpath("//*[@id=\"1360140451359\"]/div/div/div/text()")
                                article_date=article_date[0][12:-6]
                                d = datetime.datetime.strptime(article_date, '%a, %d %b %Y %I:%M %p')
                                article_date= datetime.date.strftime(d, reqd_fmt)
                                main_article=""
                                for article in articles:
                                    if article!="\n" and not isEnglish(article.split()):
                                        main_article=main_article+article
                                main_article=main_article.replace("\"","'")
                                article_text=article_text.replace("\"","'")
                                insert_query="INSERT INTO  `Disease_names`.`Articles_Multi_language` (`Date` ,`Headline` ,`Article` ,`URL` ,`Source` ,`Language` ,`Category`)VALUES (\""+str(article_date)+"\",\""+article_text+"\",\""+  main_article+"\",\""+  article_url+"\",\""+  source+"\",\""+  str(lang)+"\",\""+  str(type_)+"\");"
                                execute_insert(insert_query)
                    except Exception,e :
                        print str(e)
                        
            elif source == "http://www.jagran.com" :
                while found==True :
                    try :
                        count+=1
                        page_link=source+'/news/'+type_+'-news-hindi-page'+str(count)+'.html'
                        print
                        print page_link
                        print
                        main_page=requests.get(page_link)
                        time.sleep(5)
                        main_tree = html.fromstring(main_page.text)
                        link=main_tree.xpath("//*[@id=\"1378099854971\"]/div/ul/li/h3/a/@href")
                        #print link
                        if len(link)==0:
                            found=False
                            continue
                        article_texts=main_tree.xpath("//*[@id=\"1378099854971\"]/div/ul/li/h3/a/text()")
                        article_dates=main_tree.xpath("//*[@id=\"1378099854971\"]/div/ul/li/span/text()")
                        for index in range(len(link)) :
                            article_url=link[index]
                            article_url=source+article_url
                            if article_url not in urls_done :
                                article_text=article_texts[index]
                                article_date=article_dates[index]
                                print article_url
                                main_page=requests.get(article_url)
                                time.sleep(5)
                                main_tree = html.fromstring(main_page.text)
                                articles=main_tree.xpath("//*[@id=\"1425987651970\"]/section/section/p/text()")
                                article_date=article_date[12:-6]
                                d = datetime.datetime.strptime(article_date, '%a, %d %b %Y %I:%M %p')
                                article_date= datetime.date.strftime(d, reqd_fmt)
                                main_article=""
                                for article in articles:
                                    if article!="\n" and not isEnglish(article.split()):
                                        main_article=main_article+article
                                main_article=main_article.replace("\"","'")
                                article_text=article_text.replace("\"","'")
                                insert_query="INSERT INTO  `Disease_names`.`Articles_Multi_language` (`Date` ,`Headline` ,`Article` ,`URL` ,`Source` ,`Language` ,`Category`)VALUES (\""+str(article_date)+"\",\""+article_text+"\",\""+  main_article+"\",\""+  article_url+"\",\""+  source+"\",\""+  str(lang)+"\",\""+  str(type_)+"\");"
                                execute_insert(insert_query)
                    except Exception,e :
                        print str(e)   
                    