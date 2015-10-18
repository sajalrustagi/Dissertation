# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 22:11:42 2015

@author: sajal
"""
import MySQLdb
import plotly.plotly as py
from plotly.graph_objs import *
db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()
#select_query="SELECT COUNT(*),YEAR(Date), MONTH(Date) FROM `Disease_HealthMap_Full` GROUP BY YEAR(Date), MONTH(Date) "
select_query="SELECT COUNT(*),YEAR(RELEASE_DATE) FROM `DISEASE_INFO_FULL_MODIFY` GROUP BY YEAR(RELEASE_DATE) "
select_quer_II="SELECT COUNT( * ) , DISEASE_NAME FROM  `DISEASE_INFO_FULL_MODIFY` where  RELEASE_DATE like '%2015%' GROUP BY DISEASE_NAME ORDER BY COUNT( * ) DESC LIMIT 0 , 30"
#select_quer_II="SELECT COUNT( * ) , DISEASE_NAME FROM  `DISEASE_INFO_FULL_MODIFY`  GROUP BY DISEASE_NAME ORDER BY COUNT( * ) DESC LIMIT 0 , 30"

count=[]
year=[]
try:
   cursor.execute(select_quer_II)
   results = cursor.fetchall()
   for rows in results :
       count=count+[rows[0]]
       year=year+[rows[1]]
   db.commit()
except Exception, e: 
    print repr(e)
    db.rollback()

db.close()
trace0 = Bar(x=year,
    y=count
)
layout = Layout(
    title='Yearly Promed Incidents',
    xaxis=XAxis(
        title='Year',
    ),
    yaxis=YAxis(
        title='Number of incidents',
    )
)
layout = Layout(
    title='Overall Promed Disease Incidents',
    xaxis=XAxis(
        title='Disease Name',
    ),
    yaxis=YAxis(
        title='Number of incidents',
    )
)
layout = Layout(
    title='Promed Disease Incidents in 2015',
    xaxis=XAxis(
        title='Disease Name',
    ),
    yaxis=YAxis(
        title='Number of incidents',
    )
)
data = Data([trace0])
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Titles')

#unique_url = py.plot(data, filename = 'basic-line')