## Globus Script
This Python script is used to transfer data and execute commands from a local computer to a remote cluster with a Globus connection server. The user needs to configure Globus Connect Personal on the local machine, and the remote cluster needs to have Globus Connect and Globus Compute Endpoint installed.

### Remote Cluster(eg. NYU Greene)
Request a compute node, do not deploy on login node
```bash
srun --cpus-per-task=4 --time=04:00:00 --mem=20GB --pty /bin/bash
```
```bash
python3 -m venv path/to/globus_compute_venv
source path/to/globus_compute_venv/bin/activate
```
Following command need to run in py venv
```bash
python3 -m pip install globus-compute-sdk
python3 -m pip install -U globus-compute-sdk
python3 -m pip install globus-compute-endpoint
globus-compute-endpoint configure
globus-compute-endpoint start ys4680-endpoint
```
ID of compute endpoint (compute_endpoint_ID), can be obtained by executing following command:
```bash
globus-compute-endpoint list

(globus_compute_venv) [ys4680@log-2 globus_compute_venv]$ globus-compute-endpoint list
+--------------------------------------+--------------+-----------------+
|             Endpoint ID              |    Status    |  Endpoint Name  |
+======================================+==============+=================+
| 2a4091bd-924f-4b74-b894-54d92f50f6bf | Disconnected | ys4680-endpoint |
+--------------------------------------+--------------+-----------------+
```
ID of Globus Connect Server (remote_endpoint_ID) can be found in https://app.globus.org/ -> Collections -> Greene scratch directory ->
Overview -> UUID.

### Laptop
Create a conda env, and insall globus.
```bash
conda create -n globus_env python=3.9
conda activate globus_env
conda install pip
```
```bash
pip install globus-compute-sdk globus-sdk
pip install globus-cli
```
ID of personal client (source_endpoint_ID), can be obtained by execute following command:
```bash
globus endpoint search --filter-scope my-endpoints

(globus_env) user@10-17-35-9 globus % globus endpoint search --filter-scope my-endpoints
ID                                   | Owner          | Display Name           
------------------------------------ | -------------- | -----------------------
9bc62092-4843-11ef-8dfd-19f3c8361d4f | ys4680@nyu.edu | Yuwei Sun's Macbook Air
```

(for scratch folder)
globus session consent 'urn:globus:auth:scope:transfer.api.globus.org:all[*https://auth.globus.org/scopes/7f1a1170-3e31-4241-864e-e504e736c7b8/data_access]'


### Example
All local file pathed need to be global absolute path.
Execute command on remote cluster:
```bash
python globus_job.py --command "mv /scratch/ys4680/globus_compute_venv/test.txt /scratch/ys4680/globus_compute_venv/testNew.txt"
```
Submit a slurm script on remote cluster:
```bash
python globus_job.py --local_script_path /Users/user/Desktop/HPC-IT/globus-script/demo_job.sh --remote_script_path /scratch/ys4680/globus_compute_venv/demo_job.sh
```
Copy data and execute command on remote cluster 
```bash
python globus_job.py --command "mv /scratch/ys4680/globus_compute_venv/temp/demo_job.sh /scratch/ys4680/globus_compute_venv/temp/demo_job1.sh" --local_data_path /Users/user/Desktop/HPC-IT/globus-script/temp --remote_data_path /scratch/ys4680/globus_compute_venv/temp
```

Copy data and submit slurm script on remote cluster 
```bash
python globus_job.py --local_script_path /Users/user/Desktop/HPC-IT/globus-script/demo_job.sh --remote_script_path /scratch/ys4680/globus_compute_venv/demo_job.sh --local_data_path /Users/user/Desktop/HPC-IT/globus-script/temp --remote_data_path /scratch/ys4680/globus_compute_venv/temp
```
