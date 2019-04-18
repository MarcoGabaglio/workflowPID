# workflowPID
integration of persistent identifiers in a scientific workflow engine


This module allows the submission of parallel jobs, the deposit of their results into the CSCS storage and the creation of a persistent identifier (pointing to the sotrage object) to grant the data accessibility to everyone.


The module is composed of:
* main.py (responsible for the submission of the cwl workflow jobs and logging/moving files)
* storeWriter.py (responsible for the deposit of data into the CSCS stortage and the creation of temporary url to download the data)
* autoprocedure.py (responsible of the creation of a PID with the temporary ulr created by storeWriter)

## Permissions

In order to run a workflow using this module make sure to have the followng permissions:
* create objects into the CSCS storage
* create PIDs into the CSCS domain

## Environment

You should have a virtual environment set up with:
* cwl-runner

'''
$ virtualenv myVirtualEnv
$ source myVirtualEnv/bin/activate
$ pip install cwl-runner 
'''

* openstack
'''
$ pip install -U pip setuptools
$ pip install -U python-openstackclient lxml oauthlib python-swiftclient python-heatclient
'''


A pollux enabled environment (you will need a CSCS username and the corresponging kerberos password)

'''
$ git clone https://github.com/eth-cscs/openstack
$ source openstack/cli/pollux.env
'''

