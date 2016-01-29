#!/usr/bin/env python3

import os
import re

cwd = os.path.split(os.path.realpath(__file__))[0] + '/'

def get_api_name(b):
    p = cwd+'tracer/call_name_'+str(b)+'.h'
    with open(p,'rt') as f:
         s = f.readlines()
    l = []
    for i in s:
        p1 = i.find('"')+1
        p2 = i.find('"',p1)
        l.append(i[p1:p2])
    return l

def get_funcs():
    with open(cwd+'tracer/handler.cpp','rt') as f:
        d = f.readlines()
    d = list(filter(lambda x:x!='\n',d))
    e = {'32':[],'64':[]}
    for l in d:
        r = re.match(r'void (\w+?)_(\d+)_?(\d+)?\(.+\){\n',l)
        if r != None:
            name = r.groups()[0]
            b1 = r.groups()[1]
            b2 = r.groups()[2]
            if b1 != None:
                e[b1].append(name)
            if b2 != None:
                e[b2].append(name)
    return e

if __name__=='__main__':
    print(get_funcs())
