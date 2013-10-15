#!/usr/bin/env python
# -*- Coding: utf-8 -*-
#Author: Cagil Ulusahin
#Date: October 12nd 2013
#
# 
# 
# 
#
# Sample input and output can be foun within the directory of the github project page.**  
#

import langid, getopt, sys, logging, os,
import CMUTweetTagger
import networkx as nx
import enchant
import ast
import re
import sys, getopt
from languagefiltering import gen_walk
import langid
import logging

FORMAT = '%(asctime)-15s -8s %(message)s'
logging.basicConfig(format=FORMAT,filename='tweets.log',level=logging.DEBUG)

class Reader():
    def __init__(self,path=None,format=None):
        self.format=format
        self.path=path

    # Returns lot
    def read(self,file=None):
        if self.path is not None:
            files = gen_walk(path)
            for e,f in enumerate(files):
                folder = '/'.join(f.split("/")[:-1])
                os.system("mkdir -p out/%s" %folder )
                lot = self.readFile_direct(f)
                os.remove(f)
        elif file:
            print file
            lot = self.readFile_direct(file)
        return lot

    def readFile(self,f):
        with open(file) as f: 
            for line in f:
                yield ast.literal_eval(line)[2]

    def readFile_direct(self,infile,lang='en'):
        logger = logging.LoggerAdapter(logging.getLogger('tweets'), log.ExtraInfo())
        logger.info('Started Processing : %s', infile)
        with open(infile) as f:        
            W = None
            for line in f:
                if line.split('\t')[0] == 'W':
                    W = line.split('\t')[1].strip('\n').decode('utf-8')
                    if not (W is None) | (W == 'No Post Title'):
                        if langid.classify(W)[0] == lang:                                
                            yield W
        logger.info('End Processing : %s', infile)

def main(argv):
   logger = logging.LoggerAdapter(logging.getLogger('tweets'), log.ExtraInfo())
   infile = 'test/snap.sample'
   outfile = 'test/test.graphml'
   path = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:p:",["ifile=","ofile=","path="])
   except getopt.GetoptError:
      print 'graphlib.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'graphlib.py -i <inputfile> -o <outputfile>'
         print 'graphlib.py -p <path> -o <outputfile>'
         print 'Please check in.grapml, the initial graph will be read from that file'
         print ''
         sys.exit()
      elif opt in ("-i", "--ifile"):
         infile = arg
      elif opt in ("-o", "--ofile"):
         outfile = arg
      elif opt in ("-p", "--path"):
         path = arg
      
   r = Reader(path=path)
   lot  = [unicode(a) for a in r.read(file=infile)]
   T = Tweet()
   T.getTweets(lot)
   print 'Constructed the graph now will write to file'
   logger.info('Constructed the graph now will write to file : %s', outfile)
   nx.write_graphml(T.graph,outfile)
   logger.info('Finish write to file : %s', outfile)

'''
#    nx.write_gml(T.graph,'test/test-out.gml')
#    nx.write_gpickle(T.graph,'test/test-out.pckl')
   for a in T.graph.node:
       pass #print a
   print len(T.graph.node)
   return T.graph
'''
class Tweet:
    def __init__(self,g=None):
        if g is None:
#            self.graph = nx.read_gml('test/test.gml')
            self.graph = nx.read_graphml('in.graphml')
#            self.graph = nx.read_gpickle('test/test.pckl')
            print 'Graph has been read from file'
        else:
            self.graph = g
        self.d = enchant.Dict("en_US")
    
    def getTweets(self,tweets):
        lot = CMUTweetTagger.runtagger_parse(tweets)
        #lot = [[('example', 'N', 0.979), ('tweet', 'V', 0.7763), ('1', '$', 0.9916)],
        #       [('example', 'N', 0.979), ('tweet', 'V', 0.7713), ('2', '$', 0.5832)]]

        for tweet in lot:            
            self.getTweet(tweet)

    def getTweet(self,tweet):
        #tweet = [('example', 'N', 0.979), ('tweet', 'V', 0.7763), ('1', '$', 0.9916)]
        words = []

        for w,t,c in tweet:
            if (not self.isvalid(w)) or w.startswith("http") or w.startswith("@") or w.startswith("#") or w.isdigit() or not w.isalnum():
                continue
            self.addNode(w,t)
            for x in words:
                if self.graph.has_edge(w,x):
                    # we added this one before, just increase the weight by one
                    self.graph.add_edge(w,x)
                    self.graph[w][x]['weight'] += 1
                else:
                    # new edge. add with weight=1
                    self.graph.add_edge(w,x, weight=1)
            words.append(w)

    #adds node with the pos tag t to the self.graph
    def addNode(self,w,t):
        if not self.graph.has_node(w):
            self.graph.add_node(w,ovv=False if self.d.check(w) else True)
            self.graph.node[w][t]=1
        else:
            if(self.graph.node[w].has_key(t)):
                self.graph.node[w][t] += 1
            else:
                self.graph.node[w][t] = 1

    def isvalid(self,w):
    #return true if string contains any alphanumeric keywors
        return bool(re.search('[A-Za-z0-9]', w))

if __name__ == "__main__":
    main(sys.argv[1:])    
                
            
            
            
            
        

'''    
from graph_tool.all import *
class WordGraph():
    def createGraph():
        g = Graph(directed=False)
        v1 = g.add_vertex()
        v2 = g.add_vertex()
        e = g.add_edge(v1, v2)
        vlist = g.add_vertex(10)
        weight = g.new_edge_property("double") 
        weight[e] = 3.1416
        g.edge_properties["weight"] = weight
    
    def iterate(g):
        for v in g.vertices():
            print(v)
        for e in g.edges():
            print(e)
    def save(g):
        g.save("my_graph.xml.gz")
    def load():
        g2 = load_graph("my_graph.xml.gz")
        return g2
'''