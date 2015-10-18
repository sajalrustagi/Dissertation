# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 02:22:02 2015

@author: sajal
"""

import MySQLdb
from boilerpipe.extract import Extractor
f=open ("all_articles.txt","w")
try:
    db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8'  )
except Exception, e: 
    print repr(e)

cursor = db.cursor()
sql="SELECT Distinct Article_URL FROM `Disease_HealthMap_Full` WHERE   (`Location` LIKE  \"% india\" or `Location` LIKE  \"% india %\" or `Location` LIKE  \"india %\" ) and Date > '2014-01-01' and Source like '%google%'"            
count=0

try:
   print sql
   cursor.execute(sql)
   results = cursor.fetchall()
   for rows in results :
            extract_url=rows[0]
            print extract_url
            domain=extract_url.split("/")[2]
            try :
                extractor = Extractor(extractor='ArticleExtractor', url=extract_url)
                article = extractor.getText().replace("\"","'")
                #print article
                insert_query="INSERT INTO  `Disease_names`.`URL_Article` (`Domain` ,`URL` ,`Article`)VALUES (\""+ str(domain)+"\",\""+str(extract_url)+"\",\""+article+"\");"
                print insert_query
                try:
                   cursor.execute(insert_query)
                   if count<100 :
                       f.write("\n\n"+str(extract_url)+"\n\n"+article.encode("utf-8","replace")+"\n\n")
                   count+=1
                   db.commit()
                except Exception, e: 
                    print repr(e)
                    db.rollback()
            except Exception, e: 
                print repr(e)

                 
#                    else :
#                        print "error repeat ",id_row,dbs
                    
except Exception, e: 
    print repr(e)

f.close()


