import subprocess
import os

from time import sleep
import shutil
import sys
import storeWriter
import autoprocedure
args = sys.argv



if len(args) > 2 and args[1] == '--modify':
    if len(args) <= 2:
        print('Please add the suffix you want to modify')
    else:
        prefix = args[2]
        #non ci vuole il subprocess puoi farlo create() --modify
        subprocess.call(['python', 'autoprocedure.py', '--modify', prefix])

    sys.exit()
    
initial_files=os.listdir('.')


def parseCwlConfig():
    with open('configCWL.txt') as conf_file:
        for i in conf_file.readlines():
            if i.startswith('WORKFLOW'):
                cwl=i.split('=')[1].strip()
            if i.startswith('JOBFILES'):
                yml_files=[]
                for j in i.split('=')[1].strip().split(', '):
                    yml_files.append(j)
            if i.startswith('OUTPUT_DIRECTORY'):
                outdir = i.split('=')[1].strip()

                
    return cwl, yml_files, outdir


cwl, yml_files, outdir = parseCwlConfig()



#yml_files = ['cwlResources/abdominal-job.yml']

for i in yml_files:


    with open('tmp_job', 'w') as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -C mc\n")
        fh.writelines("srun cwl-runner %s %s"%(cwl, i))

    



    jobid = subprocess.check_output(['sbatch', 'tmp_job']).split(' ')[-1].strip()

'''
    path = i.split('/')[-1]
    with open('tmp_pid_job', 'w') as f:
        f.writelines("#!/bin/bash\n")
        f.writelines("#SBATCH -C mc\n")
        f.writelines("source /users/gamarco/workflowPID/openstack/cli/pollux.env\n")
        f.writelines("srun autoprocedure.py %s.RESULT"%(path))

    
    dep =  '--dependency=afterok:%s'%jobid
    pid_job_id = subprocess.check_output(['sbatch', dep, 'tmp_pid_job']).split(' ')[-1].strip()

'''
    
print('Waiting for jobs to complete')

a=''
while 'COMPLETED' not in a:
    sleep(2)
    a = subprocess.check_output(['sacct', '-j', jobid, '--user', 'gamarco', '--format=State'])
    continue

final_files=os.listdir('.')

new_files = list(set(final_files) - set(initial_files))



num = 0
done = False
while not done:
    try:
        os.mkdir(outdir)
        done = True
    except OSError as e:
        num += 1
        if outdir[-1].isdigit():
            outdir = dirname[:-1]
        outdir += str(num)

print('Moving result and slurm log files into %s'%outdir)


outputs = []
for f in new_files:
    if '.RESULT' in f:
        outputs.append(f)
    shutil.move(f, outdir)

print(new_files)
print(outputs)


for i in outputs:
    autoprocedure.create('%s/%s'%(outdir, i)) 

    
    




