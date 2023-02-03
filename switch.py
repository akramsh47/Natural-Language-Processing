# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:32:53 2022

@author: Akram
"""

import lark,pydot,re

#Class transformer da fare

class Switch(lark.Transformer):
    
    NUMBER = int
    CNAME = str
    DIGIT = int
    
    #def assignemnt(self,args):
        #return args[1]
    def possible_var (self,args):
        
        #Some variable to define
        lista1 = args[4]
            
        if args[0]==args[4][0]:
            for i in range(1,len(lista1),1):
                if args[1]==args[4][i][0]:
                    return args[4][i][2]
                
        if args[2]==args[4][0]:
            for i in range(0,len(lista1),1):
                if args[3]==args[4][i][0]:
                    return args[4][i][2]
                
    def case (self,args):
        return args
    
    def var_name(self,args):
        return args[0]
    
    def switch(self,args):
        return args
    

source = ' x; y; switch (x) {case 0 : z=3 ; break; case 3 : z=56 ; break; default : z=65 ; break;  }'
print(">> Input string: ",source)

#I use regex to check if the input string is consistent or no.


try : 
    if re.search( "x=%d;y=%d",source)==True :
        pass
except :
    print("You forgto to assign somenting")

try: 
    if re.search("x;",source):
        source = re.sub("x;","x=0;",source)
        
    if re.search("y;",source):
        source = re.sub("y;","y=0;",source)
except : 
    print("Error ahahahahahh")

    

switch_parser = lark.Lark.open("switch.lark",rel_to=__file__,start="possible_var",parser='lalr')
result = switch_parser.parse(source)
print("\n*** Parse tree pretty print\n", result.pretty())


# print tree to PDF file
graph = lark.tree.pydot__tree_to_graph(result, "TB")
graph.write_pdf("switch.pdf")

eval_switch = Switch().transform(result)
print(">> Result: ", eval_switch)


print("\n*** Creating parser with embedded Transformer")
switch_parser = lark.Lark.open("switch.lark",rel_to=__file__,start="possible_var",parser='lalr',transformer=Switch())
result = switch_parser.parse(source)
print(">> z = ", result)