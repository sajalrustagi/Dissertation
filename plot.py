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
select_query="SELECT COUNT(*),YEAR(Date) FROM `Disease_HealthMap_Full` GROUP BY YEAR(Date) "
count=[]
year=[]
try:
   cursor.execute(select_query)
   results = cursor.fetchall()
   for rows in results :
       count=count+[rows[0]]
       year=year+[rows[1]]
   db.commit()
except Exception, e: 
    print repr(e)
    db.rollback()

db.close()
trace0 = Scatter(x=year,
    y=count
)
layout = Layout(
    title='Title of the Graph',
    xaxis=XAxis(
        title='Year',
    ),
    yaxis=YAxis(
        title='Number of incidents',
    )
)
data = Data([trace0])
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Titles')

#unique_url = py.plot(data, filename = 'basic-line')