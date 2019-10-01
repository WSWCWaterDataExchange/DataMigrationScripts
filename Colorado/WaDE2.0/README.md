
Python codes to prepare inputs for the WaDE database in csv format. The input data come from States water rights data such as DWR_Water_Right_-_Net_Amounts.csv for Colorado. 

1. sites.py: reads the water rights file (DWR_Water_Right_-_Net_Amounts.csv) and writes out the fields for the sistes.csv file
2. methods.py, variables.py, watersources.py: output methods.csv, variables.csv, and watersources.csv respectively.
3. waterallocations_par.py: runs in parllel (mpi4py) to ouput waterallocations.csv.

Before running the code, inside the source file specify the working drectory, where the input and output csv files are located.

Except the 'waterallocations_par.py', all the Python files can be run from python commond line or windows command line, 
e.g., to run methods.py:
python methods.py

To run waterallocations_par.py: 

1. Install MPI package. For windows use Microsoft MPI from https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

2. From the command line call 

mpiexec -n num_procs python waterallocations_par.py

where num_procs is the number of processes 




