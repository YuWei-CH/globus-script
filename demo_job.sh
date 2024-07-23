#!/bin/bash
#SBATCH --job-name=demo_job
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=5G

echo "Starting job at $(date)"
# Simulate a 2 mins job
sleep 120
touch ABC.txt
mv ABC.txt DEF.txt
echo "Job finished at $(date)"