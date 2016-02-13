#!/usr/bin/env python3

import os
import json
import codecs

cwd = os.path.split(os.path.realpath(__file__))[0] + '/'

def set(key,args,conds,name):
    if os.path.exists(cwd+'settings/'+key) == False:
        os.mknod(cwd+'settings/'+key)
        t = '{}'
    else:
        with open(cwd+'settings/'+key,'r') as f:
            t = f.read()
    
    with open(cwd+'settings/'+key,'w') as f:
        d = json.loads(t)
        d[name] = {}
        d[name]['args'] = args
        d[name]['conds'] = conds
        
        f.write(json.dumps(d))

if __name__=='__main__':
    pass
