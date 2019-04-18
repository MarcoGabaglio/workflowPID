#!/usr/bin/python

import openstackclient
import subprocess
import sys
from uuid import uuid1

print('WRITING TO THE STORE....ALMOST')


def create(a):
    fila = a
    print(fila)

    newname = uuid1()
    subprocess.call(['mv', str(fila), str(newname)])
    a=subprocess.check_output(['openstack', 'object', 'create', 'PID', str(newname)])
    key = uuid1()
    c=subprocess.check_output(['swift', 'tempurl', 'GET', '3600', 'https://object.cscs.ch/v1/AUTH_21e698ff1238438fabc72e5cf9d59165/PID/%s' %newname, 'MYKEY'])


    return c
    
    '''
    lines = []




    with open('/users/gamarco/workflowPID/configPID.yml') as conf_file:
        for i in conf_file.readlines():
            lines.append(i)


    for i in range(len(lines)):
        if 'URL' in lines[i]:
            lines[i] = 'URL: %s' %c


    with open('/users/gamarco/workflowPID/configPID.yml', 'w') as conf_file:
        for i in lines:
            conf_file.write(i)

    '''


