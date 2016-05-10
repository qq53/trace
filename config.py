#!/usr/bin/env python3

import os
import re
import json
import jinja2

cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = jinja2.Environment(loader = jinja2.FileSystemLoader(cwd+'templates'))

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

def get_inter_funcs():
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

def get_args_sum():
    with open(cwd+'tracer/call.h','rt') as f:
        d = f.readlines()
    flag32 = False
    for i in d:
        if i.find('BIT32') >= 0:
            flag32 = True
        if i.find('MAX_ARGS_NUM') >= 0:
            if flag32 == True:
                num32 = i.split()[-1]
                flag32 = False
            else:
                num64 = i.split()[-1]
    return {'num32':num32,'num64':num64}

def check(name,bit,conds):
    e = get_inter_funcs()
    if name in e[bit]:
        return False

    assign = ['==','>=','<=','!=']
    for c in conds:
        if c['assign'] not in assign:
            return False

    return True

def set(key,args,conds,name,bit):
    print(123)
    if check(name,bit,conds) == False:
        return False
    print(123)

    if os.path.exists(cwd+'configs/'+key) == False:
        os.mknod(cwd+'configs/'+key)
        t = '{}'
    else:
        with open(cwd+'configs/'+key,'r') as f:
            t = f.read()
    
    with open(cwd+'configs/'+key,'w') as f:
        d = json.loads(t)
        k = name+'_'+bit
        d[k] = {}
        d[k]['args'] = args
        d[k]['conds'] = conds
        
        f.write(json.dumps(d))

    make_custom_file(key)

    return True

def make_custom_file(key='1'):
    with open(cwd+'configs/'+key,'r') as f:
        d = json.loads(f.read())
    
    call32 = []
    call64 = []
    for k in d.keys():
        bit = k.split('_')[-1]
        name = k[:k.find(bit)-1]
        if bit == '32':
            call32.append(name)
        else:
            call64.append(name)

    call = []
    for k in d.keys():
        #cond
        cond_str = ''
        for j in d[k]['conds']:
            cond_str += 'GET_ARGS('+j['arg']+')'+j['assign']+j['value']+'&&'
        cond_str = cond_str[:-2]
        
        #args
        var_str = ''
        value_str = ''
        arg = d[k]['args']
        for j in range(len(arg)):
            var_str += arg[j]['format']+' '
            if arg[j]['func'] == '':
                value_str += 'GET_ARGS('+str(j+1)+'),'
            else:
                value_str += 'htol(GET_ARGS('+str(j+1)+')),'
        var_str = var_str[:-1]
        value_str = value_str[:-1]
        
        if cond_str == '':
            call.append({'var_str':var_str,'value_str':value_str,'name':k})
        else:
            call.append({'cond_str':cond_str,'var_str':var_str,'value_str':value_str,'name':k})
    
    temp = env.get_template('custom.cpp')
    r = temp.render(calls=call,calls_32=call32,calls_64=call64)
    r = r.split('\n')
    r = list(filter(lambda x:x!='\t' and x!='',r))
    r = '\n'.join(r)
    
    with open(cwd+'configs/custom.cpp','w') as f:
        f.write(r)
    
    os.chdir(cwd+'tracer/')
    os.system('bash make.sh')

def get(key='1'):
    r = ''
    with open(cwd+'configs/'+key,'r') as f:
        r = f.read()
    return r

if __name__=='__main__':
    print(get_inter_funcs())
