# workflowPID
integration of persistent identifiers in a scientific workflow engine


This module allows the submission of parallel jobs, the deposit of their results into the CSCS storage and the creation of a persistent identifier (pointing to the sotrage object) to grant the data accessibility to everyone.


The module is composed of:
* main.py (responsible for the submission of the cwl workflow jobs)
* storeWriter.py (responsible for the deposit of data into the CSCS stortage and the creation of temporary url to download the data)
* autoprocedure.py (responsible of the creation of a PID with the temporary ulr created by storeWriter)

