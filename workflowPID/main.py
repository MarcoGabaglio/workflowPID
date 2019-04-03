import subprocess
import os
import commands
from autoprocedure import create


with open('tmp_pid_job', 'w') as f:
    f.writelines("#!/bin/bash\n")
    f.writelines("#SBATCH -C mc\n")
    f.writelines("srun autoprocedure.py")



cwl = 'cwlResources/main.cwl'

yml_files = ['cwlResources/abdominal-job.yml', 'cwlResources/deformed-job.yml']

#yml_files = ['cwlResources/abdominal-job.yml']

for i in yml_files:


    with open('tmp_job', 'w') as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -C mc\n")
        fh.writelines("srun cwl-runner %s %s"%(cwl, i))






    jobid=subprocess.check_output(['sbatch', 'tmp_job']).split(' ')[-1].strip()
    dep =  '--dependency=afterok:%s'%jobid
    subprocess.call(['sbatch', dep, 'tmp_pid_job'])
