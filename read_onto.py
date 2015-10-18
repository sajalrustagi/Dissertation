# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 12:03:17 2015

@author: sajal
"""

import gfam.go.obo
parser = gfam.go.obo.Parser(open("HumanDO.obo"))
gene_ontology = {}
for stanza in parser:
    gene_ontology[stanza.tags["id"][0]] = stanza.tags

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