# -*- coding: utf-8 -*-
"""
Created on Fri May 09 18:20:50 2014

@author: rustagi
"""

from tweepy import Stream
from tweepy import StreamListener
from tweepy import OAuthHandler
import time
import json
import MySQLdb

db = MySQLdb.connect(host="localhost", user='root', db="Disease_names",use_unicode=True, passwd='sajal',charset='utf8' )
cursor = db.cursor()
class Listener (StreamListener):
   
     
     def on_data (self,data):
        try: 
         parsed_json_real = json.loads(data)
         parsed_json=parsed_json_real
         print data
         created_at_a= parsed_json['created_at']
         created_at_a=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at_a,'%a %b %d %H:%M:%S +0000 %Y'))
         print created_at_a
         ids_a= parsed_json['id_str']
         text_a= parsed_json['text']
         hashtags_a=""
         for index in range(len(parsed_json['entities']['hashtags'])) :
             if index ==0 :
                 hashtags_a=parsed_json['entities']['hashtags'][index]['text']
             else :
                 hashtags_a=hashtags_a+" , " + parsed_json['entities']['hashtags'][index]['text']
         print hashtags_a
         if 'urls' in parsed_json['entities'] :
             urls_a=""
             expanded_urls_a=""
             for index in range(len(parsed_json['entities']['urls'])) :
                 if index ==0 :
                     urls_a=parsed_json['entities']['urls'][index]['url']
                     expanded_urls_a=parsed_json['entities']['urls'][index]['expanded_url']
                 else :
                     urls_a=urls_a+" , " + parsed_json['entities']['urls'][index]['url']
                     expanded_urls_a=expanded_urls_a+" , " + parsed_json['entities']['urls'][index]['expanded_url']
             print urls_a
             print expanded_urls_a
         if 'user_mentions' in parsed_json['entities'] :
             user_mentions_a=""
             for index in range(len(parsed_json['entities']['user_mentions'])) :
                 if index ==0 :
                     user_mentions_a=parsed_json['entities']['user_mentions'][index]['screen_name']
                 else :
                     user_mentions_a=user_mentions_a+" , " + parsed_json['entities']['user_mentions'][index]['screen_name']
             print user_mentions_a
         user_id= parsed_json['user']['id_str']
         screen_name= parsed_json['user']['screen_name']
         screen_name_a=screen_name
         name= parsed_json['user']['name']
         location= parsed_json['user']['location']
         url= parsed_json['user']['url']
         description= parsed_json['user']['description']
         followers_count= parsed_json['user']['followers_count']
         friends_count= parsed_json['user']['friends_count']
         listed_count= parsed_json['user']["listed_count"]
         favourites_count= parsed_json['user']["favourites_count"]
         statuses_count= parsed_json['user']["statuses_count"]
         user_created_at= parsed_json['user']["created_at"]
         user_created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created_at,'%a %b %d %H:%M:%S +0000 %Y'))
         time_zone= parsed_json['user']["time_zone"]
         geo_enabled= parsed_json['user']["geo_enabled"]
         lang= parsed_json['user']["lang"]
         lang_a=lang
         print user_id
         print screen_name
         print name
         print location
         print url
         print description
         print followers_count
         print friends_count
         print listed_count
         print favourites_count
         print statuses_count
         print user_created_at
         print time_zone
         print geo_enabled
         print lang
         if user_id==None :
             user_id="None"
         if screen_name==None :
             screen_name="None"
         if name==None :
             name="None"
         if url==None :
             url="None"
         if location==None :
             location="None"
         if description==None :
             description="None"
         if followers_count==None :
             followers_count="None"
         if friends_count==None :
             friends_count="None"
         if listed_count==None :
             listed_count="None"
         if favourites_count==None :
             favourites_count="None"
         if statuses_count==None :
             statuses_count="None"
         if user_created_at==None :
             user_created_at="None"
         if time_zone==None :
             time_zone="None"
         if geo_enabled==None :
             geo_enabled="None"
         if lang==None :
             lang="None"
         
         quoted_id=""
         print text_a
         insert_user_query="INSERT INTO `Disease_Tweets_UserName` (`User_ID` ,`Screen_Name` ,`Name` ,`Location`,`URL` ,`Description` ,`Followers_Count` ,`Friends_Count` ,`Listed_Count` ,`Favourites_Count` ,`Statuses_Count` ,`Created_At` ,`Time_Zone` ,`Geo_Enabled` ,`Lang`) Values ( \""+user_id + "\" , \""+screen_name +"\" , \""+name +"\" , \""+ location +"\" , \""+url + "\" , \""+description +"\","+str(followers_count) +" , "+str(friends_count) + " , "+str(listed_count) +" , "+str(favourites_count) +" , "+ str(statuses_count) + " , STR_TO_DATE (\""+ user_created_at +"\", '%Y-%m-%d %T') , \""+time_zone +"\" , \""+str(geo_enabled) + "\" , \""+lang +"\""+");"
         #insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID) Values ( " + "" + ");"
         #print insert_user_query 
         try :
           cursor.execute(insert_user_query)
           print insert_user_query
           db.commit()
         except Exception, e: 
           print  "\nERROR\n" + str(e) +"here -:" + insert_user_query
           db.rollback()
         
         if 'quoted_status' in parsed_json_real :
             parsed_json=parsed_json_real['quoted_status']
             print '\nquoted_status'
             created_at= parsed_json['created_at']
             created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
             print created_at
             ids= parsed_json['id_str']
             quoted_id=ids
             text= parsed_json['text']
             hashtags=""
             for index in range(len(parsed_json['entities']['hashtags'])) :
                 if index ==0 :
                     hashtags=parsed_json['entities']['hashtags'][index]['text']
                 else :
                     hashtags=hashtags+" , " + parsed_json['entities']['hashtags'][index]['text']
             print hashtags
             if 'urls' in parsed_json['entities'] :
                 urls=""
                 expanded_urls=""
                 for index in range(len(parsed_json['entities']['urls'])) :
                     if index ==0 :
                         urls=parsed_json['entities']['urls'][index]['url']
                         expanded_urls=parsed_json['entities']['urls'][index]['expanded_url']
                     else :
                         urls=urls+" , " + parsed_json['entities']['urls'][index]['url']
                         expanded_urls=expanded_urls+" , " + parsed_json['entities']['urls'][index]['expanded_url']
                 print urls
                 print expanded_urls
             if 'user_mentions' in parsed_json['entities'] :
                 user_mentions=""
                 for index in range(len(parsed_json['entities']['user_mentions'])) :
                     if index ==0 :
                         user_mentions=parsed_json['entities']['user_mentions'][index]['screen_name']
                     else :
                         user_mentions=user_mentions+" , " + parsed_json['entities']['user_mentions'][index]['screen_name']
                 print user_mentions
             user_id= parsed_json['user']['id_str']
             screen_name= parsed_json['user']['screen_name']
             name= parsed_json['user']['name']
             location= parsed_json['user']['location']
             url= parsed_json['user']['url']
             description= parsed_json['user']['description']
             followers_count= parsed_json['user']['followers_count']
             friends_count= parsed_json['user']['friends_count']
             listed_count= parsed_json['user']["listed_count"]
             favourites_count= parsed_json['user']["favourites_count"]
             statuses_count= parsed_json['user']["statuses_count"]
             user_created_at= parsed_json['user']["created_at"]
             user_created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created_at,'%a %b %d %H:%M:%S +0000 %Y'))
             time_zone= parsed_json['user']["time_zone"]
             geo_enabled= parsed_json['user']["geo_enabled"]
             lang= parsed_json['user']["lang"]
             print user_id
             print screen_name
             print name
             print location
             print url
             print description
             print followers_count
             print friends_count
             print listed_count
             print favourites_count
             print statuses_count
             print user_created_at
             print time_zone
             print geo_enabled
             print lang
             if user_id==None :
                 user_id="None"
             if screen_name==None :
                 screen_name="None"
             if name==None :
                 name="None"
             if url==None :
                 url="None"
             if location==None :
                 location="None"
             if description==None :
                 description="None"
             if followers_count==None :
                 followers_count="None"
             if friends_count==None :
                 friends_count="None"
             if listed_count==None :
                 listed_count="None"
             if favourites_count==None :
                 favourites_count="None"
             if statuses_count==None :
                 statuses_count="None"
             if user_created_at==None :
                 user_created_at="None"
             if time_zone==None :
                 time_zone="None"
             if geo_enabled==None :
                 geo_enabled="None"
             if lang==None :
                 lang="None"
             print text
             insert_user_query="INSERT INTO `Disease_Tweets_UserName` (`User_ID` ,`Screen_Name` ,`Name` ,`Location`,`URL` ,`Description` ,`Followers_Count` ,`Friends_Count` ,`Listed_Count` ,`Favourites_Count` ,`Statuses_Count` ,`Created_At` ,`Time_Zone` ,`Geo_Enabled` ,`Lang`) Values ( \""+user_id + "\" , \""+screen_name +"\" , \""+name +"\" , \""+ location +"\" , \""+url + "\" , \""+description +"\","+str(followers_count) +" , "+str(friends_count) + " , "+str(listed_count) +" , "+str(favourites_count) +" , "+ str(statuses_count) + " , STR_TO_DATE (\""+ user_created_at +"\", '%Y-%m-%d %T') , \""+time_zone +"\" , \""+str(geo_enabled) + "\" , \""+lang +"\""+");"
             insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID, Lang) Values (   STR_TO_DATE (\""+ created_at +"\", '%Y-%m-%d %T') , \"" + ids +"\", \"" + text +"\", \"" + screen_name +"\", \"" + urls +"\", \"" + expanded_urls +"\", \"" +user_mentions +"\", \"" +hashtags +"\"" + " , \"\" , \"\" , \""+lang +"\" );"
#             print insert_user_query 
#             print insert_query
         
             try :
               cursor.execute(insert_user_query)
               print insert_user_query
               db.commit()
             except Exception, e: 
               print  "\nERROR\n" + str(e) +"here -:" + insert_user_query
               db.rollback()
              
             try :
               cursor.execute(insert_query)
               print insert_query
               db.commit()
             except Exception, e: 
               print  "\nERROR\n" + str(e) +"here -:" + insert_query
               db.rollback()
         retweet_id=""
         
         if 'retweeted_status' in parsed_json_real :
             print "Retweet"
#             print parsed_json['retweeted_status']['created_at']
#             print parsed_json['retweeted_status']['id']
#             print parsed_json['retweeted_status']['text']
#             hashtags=""
#             for index in range(len(parsed_json['retweeted_status']['entities']['hashtags'])) :
#                 hashtags=hashtags+" , " +  parsed_json['retweeted_status']['entities']['hashtags'][index]['text']
#             print hashtags
#             print parsed_json['retweeted_status']['user']['id']
#             print parsed_json['retweeted_status']['user']['screen_name']
#             print parsed_json['retweeted_status']['user']['name']
#             print parsed_json['retweeted_status']['user']['location']
#             print parsed_json['retweeted_status']['user']['url']
#             print parsed_json['retweeted_status']['user']['description']
#             print parsed_json['retweeted_status']['user']['followers_count']
#             print parsed_json['retweeted_status']['user']['friends_count']
#             print parsed_json['retweeted_status']['user']["listed_count"]
#             print parsed_json['retweeted_status']['user']["favourites_count"]
#             print parsed_json['retweeted_status']['user']["statuses_count"]
#             print parsed_json['retweeted_status']['user']["created_at"]
#             print parsed_json['retweeted_status']['user']["time_zone"]
#             print parsed_json['retweeted_status']['user']["geo_enabled"]
#             print parsed_json['retweeted_status']['user']["lang"]
             parsed_json=parsed_json_real['retweeted_status']
             created_at_r= parsed_json['created_at']
             created_at_r=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at_r,'%a %b %d %H:%M:%S +0000 %Y'))
             print created_at_r
             ids_r= parsed_json['id_str']
             retweet_id=ids_r
             text_r= parsed_json['text']
             hashtags_r=""
             for index in range(len(parsed_json['entities']['hashtags'])) :
                 if index ==0 :
                     hashtags_r=parsed_json['entities']['hashtags'][index]['text']
                 else :
                     hashtags_r=hashtags_r+" , " + parsed_json['entities']['hashtags'][index]['text']
             print hashtags_r
             if 'urls' in parsed_json['entities'] :
                 urls_r=""
                 expanded_urls_r=""
                 for index in range(len(parsed_json['entities']['urls'])) :
                     if index ==0 :
                         urls_r=parsed_json['entities']['urls'][index]['url']
                         expanded_urls_r=parsed_json['entities']['urls'][index]['expanded_url']
                     else :
                         urls_r=urls_r+" , " + parsed_json['entities']['urls'][index]['url']
                         expanded_urls_r=expanded_urls_r+" , " + parsed_json['entities']['urls'][index]['expanded_url']
                 print urls_r
                 print expanded_urls_r
             if 'user_mentions' in parsed_json['entities'] :
                 user_mentions_r=""
                 for index in range(len(parsed_json['entities']['user_mentions'])) :
                     if index ==0 :
                         user_mentions_r=parsed_json['entities']['user_mentions'][index]['screen_name']
                     else :
                         user_mentions_r=user_mentions_r+" , " + parsed_json['entities']['user_mentions'][index]['screen_name']
                 print user_mentions_r
             user_id= parsed_json['user']['id_str']
             screen_name= parsed_json['user']['screen_name']
             screen_name_r=screen_name
             name= parsed_json['user']['name']
             location= parsed_json['user']['location']
             url= parsed_json['user']['url']
             description= parsed_json['user']['description']
             followers_count= parsed_json['user']['followers_count']
             friends_count= parsed_json['user']['friends_count']
             listed_count= parsed_json['user']["listed_count"]
             favourites_count= parsed_json['user']["favourites_count"]
             statuses_count= parsed_json['user']["statuses_count"]
             user_created_at= parsed_json['user']["created_at"]
             user_created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created_at,'%a %b %d %H:%M:%S +0000 %Y'))
             time_zone= parsed_json['user']["time_zone"]
             geo_enabled= parsed_json['user']["geo_enabled"]
             lang= parsed_json['user']["lang"]
             lang_r=lang
             quoted_id_re=""
             print user_id
             print screen_name
             print name
             print location
             print url
             print description
             print followers_count
             print friends_count
             print listed_count
             print favourites_count
             print statuses_count
             print user_created_at
             print time_zone
             print geo_enabled
             print lang
             if user_id==None :
                 user_id="None"
             if screen_name==None :
                 screen_name="None"
             if name==None :
                 name="None"
             if url==None :
                 url="None"
             if location==None :
                 location="None"
             if description==None :
                 description="None"
             if followers_count==None :
                 followers_count="None"
             if friends_count==None :
                 friends_count="None"
             if listed_count==None :
                 listed_count="None"
             if favourites_count==None :
                 favourites_count="None"
             if statuses_count==None :
                 statuses_count="None"
             if user_created_at==None :
                 user_created_at="None"
             if time_zone==None :
                 time_zone="None"
             if geo_enabled==None :
                 geo_enabled="None"
             if lang==None :
                 lang="None"
             print text_r
             insert_user_query="INSERT INTO `Disease_Tweets_UserName` (`User_ID` ,`Screen_Name` ,`Name` ,`Location`,`URL` ,`Description` ,`Followers_Count` ,`Friends_Count` ,`Listed_Count` ,`Favourites_Count` ,`Statuses_Count` ,`Created_At` ,`Time_Zone` ,`Geo_Enabled` ,`Lang`) Values ( \""+user_id + "\" , \""+screen_name +"\" , \""+name +"\" , \""+ location +"\" , \""+url + "\" , \""+description +"\","+str(followers_count) +" , "+str(friends_count) + " , "+str(listed_count) +" , "+str(favourites_count) +" , "+ str(statuses_count) + " , STR_TO_DATE (\""+ user_created_at +"\", '%Y-%m-%d %T') , \""+time_zone +"\" , \""+str(geo_enabled) + "\" , \""+lang +"\""+");"
             #insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID) Values ( " + "" + ");"
#             print insert_user_query 
             try :
               cursor.execute(insert_user_query)
               print insert_user_query
               db.commit()
             except Exception, e: 
               print  "\nERROR\n" + str(e) +"here -:" + insert_user_query
               db.rollback()
             
             quoted_id_re=""
             if 'quoted_status' in parsed_json :
                 print "Retweet Quoted"
                 parsed_json=parsed_json['quoted_status']
                 created_at= parsed_json['created_at']
                 created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
                 print created_at
                 ids= parsed_json['id_str']
                 quoted_id=ids
                 quoted_id_re=ids
                 text= parsed_json['text']
                 hashtags=""
                 for index in range(len(parsed_json['entities']['hashtags'])) :
                     if index ==0 :
                         hashtags=parsed_json['entities']['hashtags'][index]['text']
                     else :
                         hashtags=hashtags+" , " + parsed_json['entities']['hashtags'][index]['text']
                 print hashtags
                 if 'urls' in parsed_json['entities'] :
                     urls=""
                     expanded_urls=""
                     for index in range(len(parsed_json['entities']['urls'])) :
                         if index ==0 :
                             urls=parsed_json['entities']['urls'][index]['url']
                             expanded_urls=parsed_json['entities']['urls'][index]['expanded_url']
                         else :
                             urls=urls+" , " + parsed_json['entities']['urls'][index]['url']
                             expanded_urls=expanded_urls+" , " + parsed_json['entities']['urls'][index]['expanded_url']
                     print urls
                     print expanded_urls
                 if 'user_mentions' in parsed_json['entities'] :
                     user_mentions=""
                     for index in range(len(parsed_json['entities']['user_mentions'])) :
                         if index ==0 :
                             user_mentions=parsed_json['entities']['user_mentions'][index]['screen_name']
                         else :
                             user_mentions=user_mentions+" , " + parsed_json['entities']['user_mentions'][index]['screen_name']
                     print user_mentions
                 user_id= parsed_json['user']['id_str']
                 screen_name= parsed_json['user']['screen_name']
                 name= parsed_json['user']['name']
                 location= parsed_json['user']['location']
                 url= parsed_json['user']['url']
                 description= parsed_json['user']['description']
                 followers_count= parsed_json['user']['followers_count']
                 friends_count= parsed_json['user']['friends_count']
                 listed_count= parsed_json['user']["listed_count"]
                 favourites_count= parsed_json['user']["favourites_count"]
                 statuses_count= parsed_json['user']["statuses_count"]
                 user_created_at= parsed_json['user']["created_at"]
                 user_created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(user_created_at,'%a %b %d %H:%M:%S +0000 %Y'))
                 time_zone= parsed_json['user']["time_zone"]
                 geo_enabled= parsed_json['user']["geo_enabled"]
                 lang= parsed_json['user']["lang"]
                 print user_id
                 print screen_name
                 print name
                 print location
                 print url
                 print description
                 print followers_count
                 print friends_count
                 print listed_count
                 print favourites_count
                 print statuses_count
                 print user_created_at
                 print time_zone
                 print geo_enabled
                 print lang
                 if user_id==None :
                     user_id="None"
                 if screen_name==None :
                     screen_name="None"
                 if name==None :
                     name="None"
                 if url==None :
                     url="None"
                 if location==None :
                     location="None"
                 if description==None :
                     description="None"
                 if followers_count==None :
                     followers_count="None"
                 if friends_count==None :
                     friends_count="None"
                 if listed_count==None :
                     listed_count="None"
                 if favourites_count==None :
                     favourites_count="None"
                 if statuses_count==None :
                     statuses_count="None"
                 if user_created_at==None :
                     user_created_at="None"
                 if time_zone==None :
                     time_zone="None"
                 if geo_enabled==None :
                     geo_enabled="None"
                 if lang==None :
                     lang="None"
                 print text
                 insert_user_query="INSERT INTO `Disease_Tweets_UserName` (`User_ID` ,`Screen_Name` ,`Name` ,`Location`,`URL` ,`Description` ,`Followers_Count` ,`Friends_Count` ,`Listed_Count` ,`Favourites_Count` ,`Statuses_Count` ,`Created_At` ,`Time_Zone` ,`Geo_Enabled` ,`Lang`) Values ( \""+user_id + "\" , \""+screen_name +"\" , \""+name +"\" , \""+ location +"\" , \""+url + "\" , \""+description +"\","+str(followers_count) +" , "+str(friends_count) + " , "+str(listed_count) +" , "+str(favourites_count) +" , "+ str(statuses_count) + " , STR_TO_DATE (\""+ user_created_at +"\", '%Y-%m-%d %T') , \""+time_zone +"\" , \""+str(geo_enabled) + "\" , \""+lang +"\""+");"
                 insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID , Lang) Values (   STR_TO_DATE (\""+ created_at +"\", '%Y-%m-%d %T') , \"" + ids +"\", \"" + text +"\", \"" + screen_name +"\", \"" + urls +"\", \"" + expanded_urls +"\", \"" +user_mentions +"\", \"" +hashtags +"\"" + " , \"\" , \"\" , \""+lang +"\" );"
#                 print insert_user_query 
#                 print insert_query
                 try :
                   cursor.execute(insert_user_query)
                   print insert_user_query
                   db.commit()
                 except Exception, e: 
                   print  "\nERROR\n" + str(e) +"here -:" + insert_user_query
                   db.rollback()
                  
                 try :
                   cursor.execute(insert_query)
                   print insert_query
                   db.commit()
                 except Exception, e: 
                   print  "\nERROR\n" + str(e) +"here -:" + insert_query
                   db.rollback()
             insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID, Lang) Values (   STR_TO_DATE (\""+ created_at_r +"\", '%Y-%m-%d %T') , \"" + ids_r +"\", \"" + text_r +"\", \"" + screen_name_r +"\", \"" + urls_r +"\", \"" + expanded_urls_r +"\", \"" +user_mentions_r +"\", \"" +hashtags_r +"\"" + " , \""+quoted_id_re+"\" , \"\" , \""+lang_r +"\" );"
#             print insert_query    
             try :
               cursor.execute(insert_query)
               print insert_query
               db.commit()
             except Exception, e: 
               print  "\nERROR\n" + str(e) +"here -:" + insert_query
               db.rollback()
         insert_query="INSERT INTO Disease_Tweets ( Created_at , ID ,Tweet , Screen_Name , Urls , Expanded_Urls, User_Mentions , Hashtags , Quoted_Tweet_ID , Retweet_ID, Lang) Values (   STR_TO_DATE (\""+ created_at_a +"\", '%Y-%m-%d %T') , \"" + ids_a +"\", \"" + text_a+"\", \"" + screen_name_a +"\", \"" + urls_a +"\", \"" + expanded_urls_a  +"\", \"" +user_mentions_a  +"\", \"" +hashtags_a  +"\"" + " , \""+quoted_id+"\" , \"" + retweet_id + "\" , \""+lang_a +"\" );"
#         print insert_query              
         try :
               cursor.execute(insert_query)
               print insert_query
               db.commit()
         except Exception, e: 
               print "\nERROR\n" + str(e) +"here -:" + insert_query
               db.rollback()
         
 
        except BaseException, e:
         print 'failed',str(e)
         time.sleep(5)
         
     def on_error (self,error):
         print error

akey='pokbTPHcm3NVT9jwW3KBRgVvl'
asecret='Pc2EjIwN0JxaYhDpHEAwRjbgrvVWODS1PyM2ERUVAJAYNxstiT'
tkey='2485206642-0RBFbCJpqOAPeagq2kI4a0VRYdZPUi61NpSoSNV'
tsecret='Rs47fm7IGIXPDkz8OlG3H4YhFCfdT4dDLthZVIBjHxU7F'
auth=OAuthHandler(akey,asecret) 
auth.set_access_token(tkey,tsecret)
twitterstream=Stream(auth,Listener())
#print "yo"
while True :
    try :
        twitterstream.filter(track=["ebola"])
    
    except :
        print "Sorry"
       
         