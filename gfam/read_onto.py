# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 12:03:17 2015

@author: sajal
"""
import MySQLdb
try:
    db = MySQLdb.connect("localhost","root","sajal","Disease_names" )
except Exception, e: 
    print repr(e)

cursor = db.cursor()
import gfam.go.obo
parser = gfam.go.obo.Parser(open("/home/sajal/Desktop/diseaseontology/HumanDO.obo"))
gene_ontology = {}
for stanza in parser:
    gene_ontology[stanza.tags["id"][0]] = stanza.tags
list_keys=[]
for keys in gene_ontology :
    #print
    #print str(keys).split(":")
    #print
    is_a_=''
    xref_=''
    synonym_=''
    id_=''
    name_=''
    is_obsolete_=''
    alt_id_=''
    subset_=''
    def_=''
    creation_date_=''
    created_by_=''
    comment_=''
    if 'subset' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['subset'])):
        if index==0:
          subset_=str(gene_ontology[keys]['subset'][index])
        else :
          subset_=subset_ + ',' +str(gene_ontology[keys]['subset'][index])
    if 'is_obsolete' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['is_obsolete'])):
        if index==0:
          is_obsolete_=str(gene_ontology[keys]['is_obsolete'][index])
        else :
          is_obsolete_=is_obsolete_ + ',' +str(gene_ontology[keys]['is_obsolete'][index])
    if 'synonym' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['synonym'])):
        if index==0:
          synonym_=str(gene_ontology[keys]['synonym'][index])
        else :
          synonym_=synonym_ + ',' +str(gene_ontology[keys]['synonym'][index])
    if 'id' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['id'])):
        if index==0:
          id_=str(gene_ontology[keys]['id'][index])
        else :
          id_=id_ + ',' +str(gene_ontology[keys]['id'][index])
    if 'name' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['name'])):
        if index==0:
          name_=str(gene_ontology[keys]['name'][index])
        else :
          name_=name_ + ',' +str(gene_ontology[keys]['name'][index])
    if 'comment' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['comment'])):
        if index==0:
          comment_=str(gene_ontology[keys]['comment'][index])
        else :
          comment_=comment_ + ',' +str(gene_ontology[keys]['comment'][index])
    if 'xref' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['xref'])):
        if index==0:
          xref_=str(gene_ontology[keys]['xref'][index])
        else :
          xref_=xref_ + ',' +str(gene_ontology[keys]['xref'][index])
    if 'is_a' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['is_a'])):
        if index==0:
          is_a_=str(gene_ontology[keys]['is_a'][index])
        else :
          is_a_=is_a_ + ',' +str(gene_ontology[keys]['is_a'][index])
    if 'def' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['def'])):
        if index==0:
          def_=str(gene_ontology[keys]['def'][index]).replace("\"","'")
        else :
          def_=def_ + ',' +str(gene_ontology[keys]['def'][index]).replace("\"","'")
    if 'alt_id' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['alt_id'])):
        if index==0:
          alt_id_=str(gene_ontology[keys]['alt_id'][index])
        else :
          alt_id_=alt_id_ + ',' +str(gene_ontology[keys]['alt_id'][index])
    if 'created_by' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['created_by'])):
        if index==0:
          created_by_=str(gene_ontology[keys]['created_by'][index])
        else :
          created_by_=created_by_ + ',' +str(gene_ontology[keys]['created_by'][index])
    if 'creation_date' in gene_ontology[keys] :
      for index in range(len(gene_ontology[keys]['creation_date'])):
        if index==0:
          creation_date_=str(gene_ontology[keys]['creation_date'][index])
        else :
          creation_date_=creation_date_ + ',' +str(gene_ontology[keys]['creation_date'][index])
#    print
#    print 'xref_',xref_
#    print 'synonym_',synonym_
#    print 'name_',name_
#    print 'is_a_',is_a_
#    print 'id_',id_
#    print 'def_',def_
#    print 'comment_',comment_
#    print 'subset_',subset_
#    print 'is_obsolete_',is_obsolete_
#    print 'alt_id_',alt_id_
#    print 'created_by_',created_by_
#    print 'creation_date_',creation_date_
#    print
    for key in gene_ontology[keys]:
        if key not in list_keys :
            list_keys=list_keys+ [key]
        #print key
                
#        print gene_ontology[keys][key]
        
#    print
    insert_query="INSERT INTO  `Disease_names`.`Ontology_Disease_Name_First` (`id` ,`is_a` ,`name` ,`def` ,`synonym` ,`subset` ,`xref` ,`created_by` ,`creation_date` ,`is_obsolete` ,`comment` ,`alt_id`) VALUES (\""+id_+"\" , \""+is_a_+"\" ,\""+name_+"\" ,\""+def_+"\" ,\""+synonym_+"\" ,\""+subset_+"\" ,\""+xref_+"\" ,\""+created_by_+"\" ,\""+creation_date_+"\" ,\""+is_obsolete_+"\" ,\""+comment_+"\" ,\""+alt_id_+"\");"
    try:
       cursor.execute(insert_query)
       db.commit()
    except Exception, e:
        print insert_query
        print repr(e)
        db.rollback()
#    print
    
db.close()
#for item in list_keys :
#    print item+"_=''"
#for item in list_keys :
#    print "print '"+item+"_',"+item+"_"
#for item in list_keys :
#    print "if '"+item+"' in gene_ontology[keys] :\n  for index in range(len(gene_ontology[keys]['"+item+"'])):\n    if index==0:\n      "+item+"_="+"str(gene_ontology[keys]"+"['"+item+"'][index])\n    else :\n      "+item+"_="+item+"_ + ',' +str(gene_ontology[keys]"+"['"+item+"'][index])"
#import rdflib
#g=rdflib.Graph()
#g.load('/home/sajal/Desktop/diseaseontology/owlapi.xrdf')
#
#for s,p,o in g:
#  print 
#  print s
#  print p
#  print o
#  print
#
#from orangecontrib.bio.ontology import OBOParser
#parser = OBOParser("/home/sajal/Desktop/diseaseontology/HumanDO.obo")
#for event, value in parser:
#     print(event, value)