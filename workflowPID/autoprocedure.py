#!/usr/bin/python

import subprocess
import os
import json
import sys
from uuid import uuid1
import ast
import storeWriter


args = sys.argv



def parsePidConfig():
    with open('configPID.yml') as conf_file:
        for i in conf_file.readlines():
            if i.startswith('URL'):
                URL=i[i.index(': ')+1:].strip()
            if i.startswith('PREFIX'):
                prefix=i[i.index(': ')+1:].strip()
            if i.startswith('USERNAME'):
                username=i[i.index(': ')+1:].strip()
            if i.startswith('FILEKEY'):
                filekey=i[i.index(': ')+1:].strip()
            if i.startswith('DESCRIPTION'):
                description=i[i.index(': ')+1:].strip()
                
                
                
    return URL, prefix, username, filekey, description



def modify(switch):
    info = args[3:]
    prefix = parsePidConfig()[1]
    for i in info:
        if i.startswith('index') or i.startswith('--index'):
            index = i.split('=')[1]
        if i.startswith('type'):
            typ = i.split('=')[1]
        if i.startswith('value'):
            value = i.split('=')[1]


    handleurl = "https://handle01.cscs.ch:8000/api/handles/%s/%s"%(prefix, args[2])


    currentjson = subprocess.check_output(['/usr/bin/curl', '-X', 'GET', handleurl])

    currentjson = ast.literal_eval(currentjson)

    #questa parte sarebbe diversa
    if switch == 'index':
        #modificalo qua
        print(index)
        for i in range(len(currentjson['values'])):
            if (currentjson['values'][i]['index'] == int(index)):
                try:
                    if value:
                        currentjson['values'][i]['data']['value'] = value
                except:
                    pass
                try:
                    if typ:
                        print('AAAAAAA')
                        currentjson['values'][i]['type'] = typ
                except:
                    pass
            
              

    else:
        template =  {"index": index, "type": typ, "data": {"value": value, "format": "string"}}
        currentjson['values'].append(template)

    
    with open('create.json', 'w') as json_file:
        json.dump(currentjson, json_file)


    subprocess.call(['/usr/bin/curl', '--insecure', '--key', 'certificates/tmp1', '--cert', 'certificates/tmp3', '-H', 'Authorization: Handle clientCert=true', '-H', 'content-type:application/json', '--data-binary', '@create.json', '-X' , 'PUT', handleurl])

    
def create(a):

    URL, prefix, username, filekey, description = parsePidConfig()

    suffix = uuid1()

    pathToFile = a

    URL = storeWriter.create(pathToFile)

    print(pathToFile)
    
    with open('createDEFAULT.json') as json_file:
        data = json.load(json_file)
        
        data[0]['data']['value'] = URL
        data[1]['data']['value'] = description

            
    with open('create.json', 'w') as json_file:

        json.dump(data, json_file)
                
    filepem = 'tmp1'
    subprocess.call(['/users/gamarco/handle-9.0.3/bin/hdl-convert-key', filekey, '-o', filepem])

    
    combo = '/CN=300:%s\/%s'%(prefix, username)
    cert_and_public = 'tmp2'
    subprocess.call(['openssl', 'req', '-pubkey', '-x509', '-new', '-sha256', '-subj', combo, '-days', '3652', '-key', filepem, '-out', cert_and_public])

    cert = 'tmp3'
    subprocess.call(['openssl', 'x509', '-inform', 'PEM', '-in', cert_and_public, '-out', cert])
    
    handleurl = "https://handle01.cscs.ch:8000/api/handles/%s/%s"%(prefix, suffix)

    #'@create.json'    
    subprocess.call(['/usr/bin/curl', '--insecure', '--key', filepem, '--cert', cert, '-H', 'Authorization: Handle clientCert=true', '-H', 'content-type:application/json', '--data-binary', '@create.json', '-X' , 'PUT', handleurl])

    try:
        with open('suffixes.txt', 'a') as out_file:
            out_file.write(str(suffix)+'\n')
    except IOError:
        with open('suffixes.txt', 'w') as out_file:
            out_file.write(str(suffix)+'\n')

    
    try:
        #provare senza shell=True (security hazard?)
        subprocess.call('mv tmp* certificates/', shell=True)
    except OSError:
        pass


if __name__ == "__main__":
    if len(args) > 3 and args[1] == '--modify':
        if args[3] == '--new_field':
            modify('addField')
        elif args[3].startswith('--index'):
            modify('index')
    else:
        create()

    
