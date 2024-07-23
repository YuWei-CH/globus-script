import subprocess
import argparse
from globus_compute_sdk import Executor

'''
command: command that will be run on remote cluster
source_endpoint_ID: UUID for Globus Connect Personal. This can be found on the Globus website.
remote_endpoint_ID: UUID for the Globus Connect endpoint for the NYU Greene scratch folder.
compute_endpoint_ID: ID for the remote compute endpoints used by Globus Compute.
'''
source_endpoint_ID = '9bc62092-4843-11ef-8dfd-19f3c8361d4f'
remote_endpoint_ID = '7f1a1170-3e31-4241-864e-e504e736c7b8'
compute_endpoint_ID = '2a4091bd-924f-4b74-b894-54d92f50f6bf'

def transfer_file(local_file_path,remote_file_path):
    '''
    Use globus transfer [OPTIONS] SOURCE_ENDPOINT_ID[:SOURCE_PATH] DEST_ENDPOINT_ID[:DEST_PATH]
    to transfer data/script from local to Greene
    '''
    transfer_command = [
        'globus', 'transfer', 
        f'{source_endpoint_ID}:{local_file_path}', 
        f'{remote_endpoint_ID}:{remote_file_path}'
    ]
    result = subprocess.run(transfer_command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise Exception("Data transfer failed")
    print("Data transfer completed.")

def submit_slurm_job(command, remote_script_path=None):
    # Slurm job
    def run_slurm_job(command, script_path):
        import os
        if command:
            return os.system(command)
        else:
            return os.system(f"sbatch {script_path}")

    # Submit
    with Executor(endpoint_id=compute_endpoint_ID) as gce:
        future = gce.submit(run_slurm_job, command, remote_script_path)
        result = future.result()
        print(f'Remote job submitted with result: {result}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer file and submit Slurm job.")
    parser.add_argument('--command', type=str, default='', help='command that will be execute on remote cluster')
    parser.add_argument('--local_script_path', type=str, default='', help='Optional Path to the local script file')
    parser.add_argument('--remote_script_path', type=str, default='', help='Optional Path to the remote script file')
    parser.add_argument('--local_data_path', type=str, default='', help='Optional path to the local data file')
    parser.add_argument('--remote_data_path', type=str, default='', help='Optional path to the remote data file')
    
    args = parser.parse_args()

    # Transfer the script file
    if args.local_script_path and args.remote_script_path:
        print(f"Coping {args.local_script_path} to {args.remote_script_path}")
        transfer_file(args.local_script_path, args.remote_script_path)
    # Optionally transfer the data file if paths are provided
    if args.local_data_path and args.remote_data_path:
        print(f"Coping {args.local_data_path} to {args.remote_data_path}")
        transfer_file(args.local_data_path, args.remote_data_path)
    # Submit the Slurm job
    print(f"Executing command or submitting job: {args.remote_script_path if args.remote_script_path else args.command}")
    submit_slurm_job(args.command, args.remote_script_path)