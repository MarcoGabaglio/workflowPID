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
```
$ virtualenv myVirtualEnv
$ source myVirtualEnv/bin/activate
$ pip install cwl-runner 
```

* openstack
```
$ pip install -U pip setuptools
$ pip install -U python-openstackclient lxml oauthlib python-swiftclient python-heatclient
```


* A pollux enabled environment (you will need a CSCS username and the corresponding kerberos password)

```
$ git clone https://github.com/eth-cscs/openstack
$ source openstack/cli/pollux.env
```

## Setup

### configCWL.yml (SISTEMARE)

* Specify the path leading to your cwl workflow
* Specify the path leading to the job files (separated by commas)
* Specify the path where you want to save your results temporarily
```
WORKFLOW_PATH=cwlResources/main.cwl
JOBFILES_PATHS=cwlResources/abdominal-job.yml, cwlResources/deformed-job.yml
OUTPUT_DIRECTORY_PATH=NUOVIRESULT
```

### configPID.yml 

* Leave some uninformative string in the URL field
* Add your user name
* Add the path leading to your private key (the public one should be in the same directory)
* Add an initial description of the data

```
URL: asdasd
PREFIX: 21.T17999
USERNAME: mvalle
FILEKEY_PATH: 21.T11.17999_mvalle_300_privkey.bin 
DESCRIPTION: my new data
```
**Do not remove** or manually modify the **create.json** or **createDEFAULT.json** files

## RUN

Once you are all setup just type:

```
python main.py
```

## Results

* Once your analysis is complete you should regain control of the shell and in you results folder you should find a text file called **suffixes.txt**.

* You can now link your data using the https://handle01.cscs.ch:8000/21.T17999/suffix link which will redirect and download the data

