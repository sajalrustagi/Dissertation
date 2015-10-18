# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 23:56:38 2015

@author: sajal
"""

import urllib2
import os
from bs4 import BeautifulSoup
def check_validity(h,level,domain_name):
    h_link=''
    if 'www.' in h:
        i=h.find('www.')
        #print 'i is',i
        h_link=h[0:i]+h[i+4:]
    else:
        h_link=h

    #print h_link,domain_name
    if domain_name in h_link:
        #print 'yes'
        cate=h_link.encode('utf-8')
        category_url=cate+'\n'
        #print category_url
        if level.has_key(category_url):
            level[category_url]=level[category_url]+1
        else:
            level[category_url]=1

    else:
        #print 'yes'
        if h_link[0]=='/':
            if domain_name[len(domain_name)-1]!='/':
                c=(domain_name+h_link+'\n').encode('utf-8')
                #if h_link=='/news/regions/middle-east/iran':
                #         print 'found category'
                #         print c
                if level.has_key(c):
                    level[c]=level[c]+1
                else:
                    level[c]=1
            else:
                l=len(domain_name)-1
                x=domain_name[:l]
                c_link=(x+h_link+'\n').encode('utf-8')
                if level.has_key(c_link):
                    level[c_link]=level[c_link]+1
                else:
                    level[c_link]=1
def find_links(link,level,d_name):
    #print domain_name
    domain_name=d_name
    if 'www.' in d_name:
        i=d_name.find('www.')
        #print 'i is',i
        domain_name=d_name[0:i]+d_name[i+4:]
    else:
        domain_name=d_name
    #print 'domain name is',domain_name
    try :
        web_page = urllib2.urlopen(link,timeout=10)
        soup = BeautifulSoup(web_page)
        c=soup.find_all('a')
        for e in c:
            try:
                l=e['href']
                if l!=link:
                    check_validity(l,level,domain_name)
            except:
                print 'error after parsing links'
                pass

    except:
        print 'error in main link'

#def cat_domains(d):
def cat_domains(domain_name):
    #d='http://www.thehindu.com'

    level1={}
    result=[]
    #print 'given domain is',domain_name
    find_links(domain_name,level1,domain_name)
    print len(level1)
    #print level1
    x=level1.keys()
    x.sort(key = lambda s: len(s),reverse=True)
    url_count=0
    if len(x)>4:
        url_count=5
    else:
        url_count=len(x)

    #print 'url_count is',url_count
    if len(x)>9:
        for i in range(0,10):
            print 'checking urls are',x[i]
            find_links(x[i],level1,domain_name)
    else:
            for i in range(0,len(x)):
                #print 'checking urls are',x[i]
                find_links(x[i],level1,domain_name)
    for k,v in level1.items():
            if v>=(url_count-1):
                result.append(k)
                #print k
    for e in result:
        print e
    return result
    
#cat_domains('http://www.globalpost.com')

#def execution(list1,id):
#    path="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
#    for s in list1:
#        print s
#        try:
#            print s
#            x=cat_domains(s)
#            #print x
#            re=''.join(x)
#            if 'http://' in s:
#                name=s[7:]
#            else:
#                name=s
#            if len(re)>0:
#                f=open(path+name+'.txt','w')
#                f.write(re)
#                f.close()
#            else:
#                no_cat_path="D://Thesis//data//domain_name//gdelt_heuristic_approach//no_cat_path//"
#                f1=open(no_cat_path+'file.txt','a+')
#                f1.write(s+'\n')
#                f1.close()
#            print s,'is completed thread is',id
#        except:
#            print 'error'
#            continue
#"""if __name__=='__main__':
#    #input path which contains the data
#    d_path1="D://Thesis//data//domain_name//indian_not_in_category_gdelt1.txt"
#    f=open(d_path1,'r')
#    temp_list=f.read().split('\n')
#    # destination path to check if file has already been processed or not
#    path1="D://Thesis//data//domain_name//gdelt_heuristic_approach_1//"
#    info=os.listdir(path1)
#    e=[]
#    domain_list=[]
#    for s in temp_list:
#        name=''
#        if 'http://' in s:
#                name=s[7:]
#        else:
#                name=s
#        if name+'.txt' not in info:
#            print s
#            e.append(s)
#    domain_list=[]
#    i=0
#    while 1:
#        if (i+100)<len(e):
#           j=i+100
#           list1=e[i:j]
#           domain_list.append(list1)
#           i=j
#        else:
#            j=i+len(e)-1
#            list1=e[i:j]
#            domain_list.append(list1)
#            break
#    j=0
#    
#    for element in domain_list:
#        id1=j+1
#        t=threading.Thread(target=execution, args = (element,id1,))
#        j=j+1
#        #t.daemon=True
#        t.start()"""
    
#indian_valid_path="D://Thesis//data//domain_name//news_sources_ranking//based_on_4inm_website//test.TXT"
indian_valid_path="test.txt"
f=open(indian_valid_path,'r')\
#this file containinig input sources
valid_sources=f.read().split("\n")


processed_files=os.listdir(os.getcwd()+"//sources")
#indian_valid=['http://www.tehelka.com']

indian_valid=[]

for element in valid_sources:
    if element.split('//')[1]+'.txt' not in processed_files:
        indian_valid.append(element)
    else:
        print element

print len(indian_valid)
for element in indian_valid:
   result=cat_domains(element)
   if result !=[] :
    result1="".join(result)
    print 'result is',result1
    
#################################################### Post Processing Begin ##########################################
    
    result_split=result1.split("\n")
    list_words=['privacy','feedback','rssfeeds','advertise','about us','contact us','subscribe','password','user','sitemap','copyright','disclaimer','archive','term service','press release','tags','register','feed']
    #print result_split
    try :
        del result_split[result_split.index((element + "/").replace("www.",""))]
    except :
            pass
    try:
        del result_split[result_split.index((element).replace("www.",""))]
    except :
            pass
    try:
        del result_split[result_split.index("")]
    except :
            pass
    #print result_split
    result_final=[]
    dict_result={}  
    
    for results in result_split:
        if results.find(".htm")==-1 and results.find("?")==-1 :
            results_split=results.split("/")
            if results_split[3] in dict_result :
                dict_result[results_split[3]]["link"]=dict_result[results_split[3]]["link"]+[results]
                dict_result[results_split[3]]["len"]=dict_result[results_split[3]]["len"]+[len(results_split)]
            else : 
                 dict_result[results_split[3]]={}
                 dict_result[results_split[3]]["link"]=[results]
                 dict_result[results_split[3]]["len"]=[len(results_split)]
    
    for keys in dict_result :
        if  4 in dict_result[keys]['len'] :
            dict_result[keys]['link']=[dict_result[keys]['link'][dict_result[keys]['len'].index(4)]]
        if len(dict_result[keys]['link'])==1 :
            result_final=result_final+dict_result[keys]['link']
        else :
            dict_list=dict_result[keys]['link']
            bool_list = [True] * len(dict_list)
            for index1 in range(len(dict_list)) :
                for index2 in range(len(dict_list)) :
                    if index1!=index2 :
                        if dict_list[index1].find(dict_list[index2]) !=-1 :
                                bool_list[index1]=False
            for index in range(len(dict_list)) :
                if bool_list[index]==True :
                    result_final=result_final+[dict_result[keys]['link'][index]]
    result_final_new=[]
    
    from nltk.corpus import stopwords
    cachedStopWords = stopwords.words("english")

    for result in result_final :
        split_result= result.split("/")
        if split_result[-1]=="":
            new_split_result=split_result[-2].replace("-"," " ).replace("_"," ").split(" ")
            bool_intersect=bool(set(new_split_result).intersection(set(cachedStopWords)))
            found=False
            for list_word in list_words :
                try :
                    split_result_clean=split_result[-2].replace("-"," " ).replace("_"," ").lower()
                    split_result_clean_space=split_result[-2].replace("-","" ).replace("_","").replace(" ","").lower()
                    if split_result_clean.find(list_word)!=-1 or split_result_clean_space.find(list_word.replace(" ",""))!=-1:
                        found=True
                except :
                    pass
            if len(split_result[-2])<40  and bool_intersect==False and found==False:
                result_final_new=result_final_new+[result]
        else :
            new_split_result=split_result[-1].replace("-"," " ).replace("_"," ").split(" ")
            bool_intersect=bool(set(new_split_result).intersection(set(cachedStopWords)))
            found=False
            for list_word in list_words :
                try :
                    split_result_clean=split_result[-1].replace("-"," " ).replace("_"," ").lower()
                    split_result_clean_space=split_result[-2].replace("-","" ).replace("_","").replace(" ","").lower()
                    if split_result_clean.find(list_word)!=-1 or split_result_clean_space.find(list_word.replace(" ",""))!=-1:
                        found=True
                except :
                    pass
            if len(split_result[-1]) <40 and bool_intersect==False and found==False:
                result_final_new=result_final_new+[result]
    result1="\n".join(result_final_new)
    print result1
    
#################################################### Post Processing Ends ##########################################            
    path1="sources//"
    domain=element.split("//")[1]
    f=open(path1+domain+'.txt','w')
    #f=open(domain+'.txt','w')
    f.write(result1)
    f.close()
#path="D:\Thesis\data\domain_name\category_gdelt_valid_source_14_April"