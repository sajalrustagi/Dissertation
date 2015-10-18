# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 23:05:28 2015

@author: sajal
"""
import requests
import MySQLdb
from time import ctime

summary=""
db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
cursor = db.cursor()


def extract_file_names (link,out) :
    #print "begin :",out
    done=False
    trying_count=0
    while  not done :
        try :
            r=requests.get(link, timeout=10)
            done=True 
        except :
              if trying_count>30 :
                  done=True 
              #print "trying to connect :",link 
              trying_count+=1
    f=open(out,"w")
    f.write(r.content)
    f.close
    #print "done :",out

def extract_incidents(out) :
    f=open(out,"r")
    lines=f.read()
#    print len(lines)
    f.close()
    main_lines=lines.split("listview\":[")
    f=open("/home/sajal/Desktop/Promed_scrap/HealthMap_Without_Results/"+out.split("/")[-1],"w")
    try :
        incidents= main_lines[1].split("],\"listview_by_alert")[0].split("],[")
        incidents[0]=incidents[0][1:]
        incidents[-1]=incidents[-1][:-1]
        for incident in incidents :
            incident_split=incident.split("<\/span>")[0:2]
            id_no=incident_split[0].split("ai.php?")[1].split("&trto")[0]
            rating=incident_split[0][-1]
#            if incident_split[0].count(",null")>2 and incident_split[0].count(",null,null,null")==0:
#                print "count null more than 2 :",incident
            if incident_split[0].find(",\"<span class=\\\"rating\\\"><span>")==-1 :
                print "rating not found :",incident
            incident_split[0]=incident_split[0][:-1].replace(",\"<span class=\\\"rating\\\"><span>","").replace(",null",",\"null\"")
            incident_split[0]=incident_split[0].split("\",\"")
            incident_split[0][0]=incident_split[0][0][1:]
            incident_split[0][-1]=incident_split[0][-1][:-1]
            incident_split[1]=incident_split[1].split(" ")[-1].replace("\\\">","")
            #print (str(incidents.index(incident)+1))
            f.write(str(incidents.index(incident)+1)+"\n"+str(incident_split[0])+"\n"+rating+"\n"+ incident_split[1]+ "\n")
            source = incident_split[0][0].split("title=\\\"")[1].split("\\\"")[0]
            date=incident_split[0][1]
            report =incident_split[0][2].split("\\\">")
            link_summary=report[0].split("\"")[1][4:-1]
            headline_report=report[1].replace("<\/a>","")
            disease=incident_split[0][3]
            location_url=incident_split[0][4].split("\\\">")
            lattitude=location_url[0].split("(")[1].split(")")[0]
            location=location_url[1][:-5]
            species=incident_split[0][5]
            cases=incident_split[0][6]
            deaths=incident_split[0][7]
            
            #for split_incident in incident_split[0] :
            #f.write( "\n" +source +"\n" +summary+"\n" + date +"\n" + link_summary +"\n" + headline_report +"\n" + disease +"\n" +  lattitude +"\n" + location +"\n" + species +"\n" + cases +"\n" + deaths +"\n" + rating +"\n" + id_no +"\n" )
            f.write( "\n" +source +"\n" +date+"\n" + disease +"\n" + location +"\n" + lattitude +"\n" + headline_report +"\n" +  summary +"\n" + link_summary +"\n" + species +"\n" + cases +"\n" + deaths +"\n" + rating +"\n" + id_no +"\n" )
            insert_query="INSERT INTO Disease_HealthMap_without ( `Source` , `Date` ,  `Disease` , `Location`, `Lattitude` , `Headline_Report` , `Summary` , `Article_URL` , `Species` ,`Cases` ,  `Death` ,  `Rating` ,  `ID` ) VALUES( \""+str(source)+"\" , STR_TO_DATE (\""+ str(date) +"\", '%d %b %Y') , \""+str(disease)+"\" , \""+str(location)+"\" , \""+str(lattitude.replace("\"","'"))+"\" , \""+str(headline_report)+"\" ,\""+str(summary.replace("\"","'"))+"\" ,\""+str(link_summary)+"\" ,\""+str(species)+"\" ,"+str(cases)+" ,"+str(deaths)+" ,"+str(rating)+" ,"+str(id_no) +" );"
            #print insert_query
            try:
               cursor.execute(insert_query)
               print insert_query
               db.commit()
            except Exception, e: 
                if str(e).find("(1062, \"Duplicate entry")==-1:
                       print str(e)
                #raw_input("Press ENTER to exit")
                db.rollback()
            #
            if len(incident_split[0]) !=8:
                print "split incident not 8 :",incident
            f.write("\n")
    except Exception,e :
            print str(e)
#    print len(main_lines[1])
#    print len(main_lines[1].split("],\"listview_by_alert")[0])
    f.close()


#link1="http://www.healthmap.org/ln.php?3592246"
#link2="http://www.healthmap.org/ai.php?3592246&trto=en&trfr=en&pid221"
#out2="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/out.html"
#link="http://www.healthmap.org/getAlerts.php?category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&sdate=01%2F01%2F2015&edate=02%2F01%2F2015&heatscore=1&partner=hm"

#end_year=2015
#start_year=2015
#last_year=1994
#end_month=8
#start_month=7
#link="http://www.healthmap.org/getAlerts.php?category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&sdate="+str(start_month)+"%2F1%2F"+str(start_year)+"&edate="+str(end_month)+"%2F1%2F"+str(end_year)+"&heatscore=1&partner=hm"
#out="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/"+str(start_month)+"-"+str(start_year)+"-to-"+str(end_month)+"-"+str(end_year)+".txt"
#extract_file_names (link,out)
#extract_incidents(out)
#while start_year>=last_year :
#     if start_month==12 :
#        end_year=end_year-1
#        start_month=start_month-1
#        end_month=12
#        link="http://www.healthmap.org/getAlerts.php?category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&sdate="+str(start_month)+"%2F1%2F"+str(start_year)+"&edate="+str(end_month)+"%2F1%2F"+str(end_year)+"&heatscore=1&partner=hm"
#        out="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/"+str(start_month)+"-"+str(start_year)+"-to-"+str(end_month)+"-"+str(end_year)+".txt"
#        print link,out
#        if os.path.isfile(out) :
#            pass
#        else :
#            extract_file_names (link,out)
#        extract_incidents(out)
#        
#     while start_month!=1 :
#        end_month=end_month-1
#        start_month=start_month-1
#        link="http://www.healthmap.org/getAlerts.php?category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&sdate="+str(start_month)+"%2F1%2F"+str(start_year)+"&edate="+str(end_month)+"%2F1%2F"+str(end_year)+"&heatscore=1&partner=hm"
#        out="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/"+str(start_month)+"-"+str(start_year)+"-to-"+str(end_month)+"-"+str(end_year)+".txt"
#        print link,out
#        if os.path.isfile(out) :
#            pass
#        else :
#            extract_file_names (link,out)
#        extract_incidents(out)
##        break
#     if start_month==1 :
#        start_year=start_year-1
#        start_month=12
#        end_month=end_month-1
#        link="http://www.healthmap.org/getAlerts.php?category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&sdate="+str(start_month)+"%2F1%2F"+str(start_year)+"&edate="+str(end_month)+"%2F1%2F"+str(end_year)+"&heatscore=1&partner=hm"
#        out="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/"+str(start_month)+"-"+str(start_year)+"-to-"+str(end_month)+"-"+str(end_year)+".txt"
#        print link,out
#        if os.path.isfile(out) :
#            pass
#        else :
#            extract_file_names (link,out)
#        extract_incidents(out)
print ctime()
link='http://www.healthmap.org/getAlerts.php?locations=&diseases=&sources=&species=&category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&vaccines=&time_interval=1+week&zoom_lat=15.000000&zoom_lon=18.000000&zoom_level=2&displayapi=&heatscore=1&partner=hm'
out="/home/sajal/Desktop/Promed_scrap/HealthMap_Alerts/out_without.txt"
extract_file_names (link,out)
extract_incidents(out)
print
db.close()
   
    
    


