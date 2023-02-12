# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:32:53 2022

@author: Akram Shimi
"""

import lark,pydot,re


class Switch(lark.Transformer):
    
    NUMBER = int
    CNAME = str
    DIGIT = int
    
    
    def case (self,args):
        return args
    
    def var_name(self,args):
        return args[0]
    
    def switch(self,args):
        return args
        
    def possible_var (self,args):
        
        #-Rememeber : args[4] it's a list containing all the leaf nodes 
        #-in order to find the right value, i have to iterate over that list
        lista1 = args[4]
            
        if args[0]==args[4][0]:
            for i in range(1,len(lista1)-1):
                if args[1]==args[4][i][0]:
                    return args[4][i][2]
                else : 
                    index = len(lista1)-1
                    return args[4][-1][1]
                
        if args[2]==args[4][0]:
            for i in range(1,len(lista1)-1):
                if args[3]==args[4][i][0]:
                    return args[4][i][2]
                else : 
                    #index = len(lista1)-1
                    return args[4][-1][1]
    

source = '''
            x=1; y = 33; 

            switch (x) { 
                case 1 : z=3 ; break; 
                case 3 : z=22; break; 
                default : z=65 ; break; 
            }
'''
            
print(">> Input string: ",source)



#I use regex to check if the input string is consistent or no.
x = re.findall('\s*x\s*;',source)
y = re.findall('\s*y\s*;',source)

#Substiute the not initilized varible with zero.
if x and y :
    source = re.sub('\s*x\s*;','x = 0;',source)
    source = re.sub('\s*y\s*;','y = 0;',source)
elif x : 
    source = re.sub('\s*x\s*;','x = 0;',source)
elif y :
    source = re.sub('\s*y\s*;','y = 0;',source)


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