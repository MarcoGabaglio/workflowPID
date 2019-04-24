#!/usr/bin/python

##########################
#    AUTOPROCEDURE.PY    # 
##########################
#This module has the purpose to create the handle used for the resolution of the PID
#Here it is also defined the writeToStore function needed to write the result file to
#the CSCS storage and genetate a temporary URL for it


import subprocess
import os
import json
import sys
from uuid import uuid1
import ast
import openstackclient
import configCreator

args = sys.argv


#rename and upload the inputfile (passed as paramenter) to the CSCS storage and create a temporary link to it
def writeToStore(a):
    fila = a

    newname = uuid1()
    subprocess.call(['mv', str(fila), str(newname)])
    a=subprocess.check_output(['openstack', 'object', 'create', 'PID', str(newname)])
    key = uuid1()
    c=subprocess.check_output(['swift', 'tempurl', 'GET', '3600', 'https://object.cscs.ch/v1/AUTH_21e698ff1238438fabc72e5cf9d59165/PID/%s' %newname, 'MYKEY'])

    subprocess.call(['rm', str(newname)])
    return c

#Parses the configPID.yml 
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


#Main function for the creation of the handle


def create(a):

    #Checks if configPID.yml is present, if it is the information is extracted.
    #If it is not present the parameters will be asked interactively and the configPID.yml file created
    try:
        URL, prefix, username, filekey, description = parsePidConfig()
    except:
        print('no config found, creating it:\n')
        configCreator.createPID()
        URL, prefix, username, filekey, description = parsePidConfig()

    #create new name
    suffix = uuid1()

    #get jobname and output directory so that we know were to put final files
    pathToFile = a
    outdir = pathToFile.split('/')[0]
    resName = pathToFile.split('/')[1]

    #deposit and get temporary url for the result file in the CSCS storage
    URL = writeToStore(pathToFile)


    #json template used to generate the create.json used to create the handle
    template = '[{"index": 1, "type": "URL", "data": {"value": "asd", "format": "string"}}, {"index": 10, "type": "Description", "data": {"value": "asdasdasd", "format": "string"}}, {"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": 300, "handle": "asd", "permissions": "011111110011"}, "format": "admin"}}]'


    #open it as json and fill with data
    template = json.loads(template)
    template[0]['data']['value'] = URL
    template[1]['data']['value'] = description
    template[2]['data']['value']['handle'] = "%s/%s"%(prefix, username)

    #write the new information to the create.json file
    with open('create.json', 'w') as json_file:
        json.dump(template, json_file)


    #certificate surgery
    filepem = 'tmp1'
    subprocess.call(['/users/gamarco/handle-9.0.3/bin/hdl-convert-key', filekey, '-o', filepem])
    combo = '/CN=300:%s\/%s'%(prefix, username)
    cert_and_public = 'tmp2'
    subprocess.call(['openssl', 'req', '-pubkey', '-x509', '-new', '-sha256', '-subj', combo, '-days', '3652', '-key', filepem, '-out', cert_and_public])
    cert = 'tmp3'
    subprocess.call(['openssl', 'x509', '-inform', 'PEM', '-in', cert_and_public, '-out', cert])

    #new url for the PID
    handleurl = "https://handle01.cscs.ch:8000/api/handles/%s/%s"%(prefix, suffix)

    #main call used to create the handle
    subprocess.call(['/usr/bin/curl', '--insecure', '--key', filepem, '--cert', cert, '-H', 'Authorization: Handle clientCert=true', '-H', 'content-type:application/json', '--data-binary', '@create.json', '-X' , 'PUT', handleurl])

    #try to append resulting suffixes to the file
    #create a new file and write suffixes to it if not present
    try:
        with open('%s/suffixes.txt'%outdir, 'a') as out_file:
            handleurl = "https://hdl.handle.net/%s/%s"%(prefix, suffix)
            out_file.write(str(resName)+'\t'+handleurl+'\n')
    except IOError:
        with open('%s/suffixes.txt'%outdir, 'w') as out_file:
            handleurl = "https://hdl.handle.net/%s/%s"%(prefix, suffix)
            out_file.write(str(resName)+'\t'+handleurl+'\n')


    #Should be in main but why not
    try:
        subprocess.call('rm tmp*', shell=True)
    except OSError:
        pass

    
