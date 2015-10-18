# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 04:24:01 2015

@author: sajal
"""
from boilerpipe.extract import Extractor
import MySQLdb
import time
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()
#list_sources=["EuroSurveillance","Moreover Technologies"]
list_sources=["Google News"]
#list_sources=["World Health Organization","Wildlife Disease Node","Ministry of Health Sites","ReliefWeb"]
sql="SELECT distinct `URL` FROM `Corpus_English`"
urls_done=[]
try :
    cursor.execute(sql)
    results = cursor.fetchall()
    for rows in results :
        urls_done=urls_done+[rows[0]]
except Exception,e :
        print "Not sql :",str(e)
        
for source in list_sources :
    print source
    if source=="World Health Organization" :
        sql="SELECT  `Date` ,  `Source` ,  `Article_URL`, `Headline_Report` FROM `Disease_HealthMap_Full` WHERE source=\""+source+"\" and Article_URL like \"%http://www.who.int/%\" and Article_URL not like \"%http://www.who.int/sorry%\" and (`Date` <\"2009-01-01\" or  `Date` >\"2009-12-31\" ) group by `Date` ,  `Source` ,  `Article_URL`,`Headline_Report`  ORDER BY `Disease_HealthMap_Full`.`Date` DESC  "    
    else :
        sql="SELECT `Date` ,  `Source` ,  `Article_URL` ,`Headline_Report` FROM `Disease_HealthMap_Full` WHERE source=\""+source+"\" group by `Date` ,  `Source` ,  `Article_URL` ,`Headline_Report`  ORDER BY `Disease_HealthMap_Full`.`Date` DESC"  
    try :
        cursor.execute(sql)
        results = cursor.fetchall()
        for rows in results :
            article=""
            extract_url=rows[2]
            date=rows[0]
            print date
            if extract_url not in urls_done:
                print extract_url
                subject=rows[3]
                try :
                    extractor = Extractor(extractor='ArticleExtractor', url=extract_url)
                    #time.sleep(10)
                    article = extractor.getText().replace("\"","'").encode("utf-8")
                except Exception,e :
                    print "Not able to extract :",str(e)
                #print article
                if article !="" :
                    insert_query="INSERT INTO `Disease_names`.`Corpus_English` (`Source`,`Date` ,`Headline` ,`Article` ,`URL`) VALUES( \""+str(source)+"\" ,STR_TO_DATE (\""+ str(date) +"\", ' %Y-%m-%d %T'),\""+str(subject)+"\" ,\""+str(article)+"\" ,\""+str(extract_url)+"\");"
                    #print insert_query                
                    try:
                       cursor.execute(insert_query)
                       db.commit()
                    except Exception, e:
                        print str(e)
                        print insert_query
                        db.rollback()
            
    except Exception,e :
        print "Not sql :",str(e)
#extract_url="http://reliefweb.int/report/liberia/liberia-ebola-situation-report-no-63-3-december-2014	"
