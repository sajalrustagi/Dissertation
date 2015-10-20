# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:04:15 2015

@author: sajal
"""
import MySQLdb,operator
db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()


sql="SELECT Word FROM `Topics_LDA_1_temp_1000` ORDER BY  `Topics_LDA_1_temp_1000`.`Probability` DESC"

words_1=[]
try :
    cursor.execute(sql)
    results = cursor.fetchall()
    for rows in results :
        words_1=words_1+[rows[0]]
except Exception,e :
        print "Not sql :",str(e)

sql="SELECT Word FROM `Topics_LDA_1000_view` ORDER BY  `Topics_LDA_1000_view`.`Probability` DESC" 
 
words_2=[]
try :
    cursor.execute(sql)
    results = cursor.fetchall()
    for rows in results :
        words_2=words_2+[rows[0]]
except Exception,e :
        print "Not sql :",str(e)

word_1_set=set(words_1)
word_2_set=set(words_2)

values_tf={}
values_df={}
for indice in range(len(tf_df_values)):
    print indice
    tf_df_value=tf_df_values[indice]
    split_tf_df_values=tf_df_value.split("+,+")
    key=split_tf_df_values[0]
    values_tf[key]=int(split_tf_df_values[1])
    values_df[key]=int(split_tf_df_values[2])

sorted_values = sorted(values_tf.items(), key=operator.itemgetter(1),reverse=True)
words_3=[]
for items in sorted_values[:1000]:
    words_3=words_3+[items[0]]

word_3_set=set(words_3)
 