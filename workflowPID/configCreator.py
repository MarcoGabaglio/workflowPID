
def createCWL():
    workflow = raw_input("specify the workflow path: ")
    jobs = raw_input("specify the jobs path: ")
    out = raw_input("specify the output directory path: ")

    with open('configCWL.yml', 'w') as f:
        f.write('WORKFLOW_PATH: %s\n' %workflow)
        f.write('JOBFILES_PATHS: %s\n' %jobs)
        f.write('OUTPUT_DIRECTORY: %s' %out)
    
    
