#!/usr/bin/python

import subprocess
import os
import json
import sys
from uuid import uuid1




def parseConfig():
    with open('config.txt') as conf_file:
        for i in conf_file.readlines():
            if i.startswith('URL'):
                URL=i.split('=')[1].strip()
            if i.startswith('PREFIX'):
                prefix=i.split('=')[1].strip()
            if i.startswith('USERNAME'):
                username=i.split('=')[1].strip()
            if i.startswith('FILEKEY'):
                filekey=i.split('=')[1].strip()
            if i.startswith('DESCRIPTION'):
                description=i.split('=')[1].strip()
                
    return URL, prefix, username, filekey, description

def create():
    URL, prefix, username, filekey, description = parseConfig()

    suffix = uuid1()
    
    with open('create.json') as json_file:
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
    #handleurl = "https://handle01.cscs.ch:8000/api/handles/%s/MarcoTest"%(prefix)
    subprocess.call(['/usr/bin/curl', '--insecure', '--key', filepem, '--cert', cert, '-H', 'Authorization: Handle clientCert=true', '-H', 'content-type:application/json', '--data-binary', "@create.json", '-X' , 'PUT', handleurl])

    try:
        with open('suffixes.txt', 'a') as out_file:
            out_file.write(str(suffix)+'\n')
    except IOError:
        with open('suffixes.txt', 'w') as out_file:
            out_file.write(str(suffix)+'\n')

    
    try:
        #provare senza shell=True (security hazard?)
        subprocess.call('mv tmp* Trash/', shell=True)
    except OSError:
        pass
   


if __name__ == "__main__":
    create()

