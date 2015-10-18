# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:38:09 2015

@author: sajal
"""
import MySQLdb
try:
    db = MySQLdb.connect("192.168.111.105","root","dhavalpatel","newsdata" )
except Exception, e: 
    print repr(e)

cursor = db.cursor()
sql="SELECT count(*) FROM hindi_news_repository"
try:
   cursor.execute(sql)
   results = cursor.fetchall()
   for rows in results :
            print rows
   db.commit()
except Exception, e: 
    print repr(e)
    db.rollback()