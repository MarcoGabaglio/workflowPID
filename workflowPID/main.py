import subprocess
import os

from time import sleep
import shutil
import sys
##########################                                                                                                                            
#        MAIN.PY         #                                                                                                                            
##########################
#This is the main module of the "package". It is responsable for submitting parallel SLURM jobs to the cluster,
#wait for them to finish and call the autoprocedure module (storage deposit and PID creation). 



import autoprocedure
args = sys.argv
import configCreator

    
#Parses the configCWL.yml file
def parseCwlConfig():
    with open('configCWL.yml') as conf_file:
        for i in conf_file.readlines():
            if i.startswith('WORKFLOW'):
                cwl=i[i.index(': ')+1:].strip()
            if i.startswith('JOBFILES'):
                yml_files=[]
                for j in i[i.index(': ')+1:].strip().split(', '):
                    yml_files.append(j)
            if i.startswith('OUTPUT_DIRECTORY'):
                outdir = i[i.index(': ')+1:].strip()
                

                
    return cwl, yml_files, outdir

#If the configCWL.yml file is not present create it with an interactive prompt
try:
    cwl, yml_files, outdir = parseCwlConfig()
except:
    print('No config found, creating it now:\n')
    configCreator.createCWL()
    cwl, yml_files, outdir = parseCwlConfig()
    

#check the state of the directory at the beginning
initial_files=os.listdir('.')

#create and submit the slurm jobs 
for i in yml_files:


    with open('tmp_job', 'w') as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -C mc\n")
        fh.writelines("srun cwl-runner %s %s"%(cwl, i))


    jobid = subprocess.check_output(['sbatch', 'tmp_job']).split(' ')[-1].strip()


    print('Submitting %s to the queue'%i)

#wait for the last submitted job to complete (improvable)
a=''
while 'COMPLETED' not in a:
    sleep(2)
    a = subprocess.check_output(['sacct', '-j', jobid, '--user', 'gamarco', '--format=State'])
    continue

#check the state of the folder afte the analysis has completed
final_files=os.listdir('.')

#get freshly created files
new_files = list(set(final_files) - set(initial_files))


#create a new result folder
#if the default name is already present add 1 then 2 ... to the defaultname
num = 0
done = False
while not done:
    try:
        os.mkdir(outdir)
        done = True
    except OSError as e:
        num += 1
        if outdir[-1].isdigit():
            outdir = outdir[:-1]
        outdir += str(num)

print('Moving result and slurm log files into %s'%outdir)

#move the files to the result folder and select non-tmp and non-slurm files as the results
outputs = []
for f in new_files:
    if 'slurm' not in f and 'suffixes' not in f and 'tmp' not in f:
        outputs.append(f)
    shutil.move(f, outdir)


#call the autoprocedure on the selected result files uploading them to the storage and generating the PID
for i in outputs:
    autoprocedure.create('%s/%s'%(outdir, i)) 

    print('Generating PID for %s'%i)
    




