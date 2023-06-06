# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:00:17 2020

@author: boczek
"""
'''
from io import open

def change_sign(txt, sign1, sign2):
    res_txt=""
    for i in txt:
        if(i == sign1):
            res_txt.join(sign2)
        else:
            res_txt.join(i)
    return res_txt

txt1=open("xmas.txt", 'r', encoding='utf-8')
k=''
for i in txt1.read():
    if(i != '\n'):
        if(i == '_'):
            k+=' '
        else:
            k+=str(i)
    else:
        print(k)
        #print('\n')
        k=''
#print(change_sign())
'''
one = 2.675
two = 0.001
res = one + two
print(res)