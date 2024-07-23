### Greene
globus-compute-endpoint start ys4680-endpoint

### Laptop
conda create -n globus_env python=3.9
conda activate globus_env
conda install pip

pip install globus-compute-sdk globus-sdk
pip install globus-cli
globus endpoint search --filter-scope my-endpoints

(for scratch folder)
globus session consent 'urn:globus:auth:scope:transfer.api.globus.org:all[*https://auth.globus.org/scopes/7f1a1170-3e31-4241-864e-e504e736c7b8/data_access]'


### Example
(Only Command)
python globus_job.py --command "mv /scratch/ys4680/globus_compute_venv/test.txt /scratch/ys4680/globus_compute_venv/testNew.txt"

(Only slurm script)
python globus_job.py --/Users/user/Desktop/HPC-IT/globus/demo_job.sh --/scratch/ys4680/globus_compute_venv/demo_job.sh

(data + slurm script)
python globus_job.py --/Users/user/Desktop/HPC-IT/globus/demo_job.sh /scratch/ys4680/globus_compute_venv/demo_job.sh --local_data_path /Users/user/Desktop/HPC-IT/globus/temp --remote_data_path /scratch/ys4680/globus_compute_venv/temp

(data + command)
python globus_job.py --command "mv /scratch/ys4680/globus_compute_venv/temp/demo_job.sh /scratch/ys4680/globus_compute_venv/temp/demo_job1.sh" --local_data_path /Users/user/Desktop/HPC-IT/globus/temp --remote_data_path /scratch/ys4680/globus_compute_venv/temp# globus-script
